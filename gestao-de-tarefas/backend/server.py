from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = os.environ.get("JWT_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create the main app without a prefix
app = FastAPI()
# ... depois de app = FastAPI()
api_router = APIRouter()


# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    password_hash: str
    is_admin: bool = False
    team_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    team_id: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    is_admin: bool
    team_id: Optional[str] = None
    created_at: datetime

class Team(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    created_by: str  # admin user id
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    responsible_user_id: str
    deadline: Optional[datetime] = None
    category: str
    urgency: str  # baixa, média, alta, crítica
    status: str = "pendente"  # pendente, em_progresso, concluida
    requested_by: str  # user id who requested
    team_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    responsible_user_id: str
    deadline: Optional[datetime] = None
    category: str
    urgency: str
    requested_by: str
    team_id: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsible_user_id: Optional[str] = None
    deadline: Optional[datetime] = None
    category: Optional[str] = None
    urgency: Optional[str] = None
    status: Optional[str] = None

class Comment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str
    user_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CommentCreate(BaseModel):
    task_id: str
    content: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Auth utilities
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = await db.users.find_one({"email": email})
        if user is None:
            raise credentials_exception
        return User(**user)
    except jwt.PyJWTError:
        raise credentials_exception

async def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Email utility
async def send_notification_email(user_email: str, task_title: str, task_description: str):
    """Send email notification (placeholder - you'll need to configure Gmail SMTP)"""
    # For now, just log the email
    logging.info(f"EMAIL NOTIFICATION: To {user_email} - New task: {task_title}")
    # TODO: Implement actual email sending with Gmail SMTP

# Auth Routes
@api_router.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user
    user_dict = user.dict()
    del user_dict["password"]
    user_dict["password_hash"] = hashed_password
    user_obj = User(**user_dict)
    
    await db.users.insert_one(user_obj.dict())
    return UserResponse(**user_obj.dict())

@api_router.post("/auth/login", response_model=Token)
async def login(user_login: UserLogin):
    user = await db.users.find_one({"email": user_login.email})
    if not user or not verify_password(user_login.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/auth/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user.dict())

# Admin Routes
@api_router.post("/admin/users", response_model=UserResponse)
async def create_user_by_admin(user: UserCreate, admin: User = Depends(get_admin_user)):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user
    user_dict = user.dict()
    del user_dict["password"]
    user_dict["password_hash"] = hashed_password
    user_obj = User(**user_dict)
    
    await db.users.insert_one(user_obj.dict())
    return UserResponse(**user_obj.dict())

@api_router.get("/admin/users", response_model=List[UserResponse])
async def get_all_users(admin: User = Depends(get_admin_user)):
    users = await db.users.find().to_list(1000)
    return [UserResponse(**user) for user in users]

# User Routes
@api_router.get("/users", response_model=List[UserResponse])
async def get_team_users(current_user: User = Depends(get_current_user)):
    """Get users from the same team as the current user"""
    if current_user.is_admin:
        # Admin can see all users
        users = await db.users.find().to_list(1000)
    else:
        # Regular users can only see users from their team
        if current_user.team_id:
            users = await db.users.find({"team_id": current_user.team_id}).to_list(1000)
        else:
            users = []
    return [UserResponse(**user) for user in users]

# Team Routes
@api_router.post("/teams", response_model=Team)
async def create_team(team: TeamCreate, admin: User = Depends(get_admin_user)):
    team_dict = team.dict()
    team_dict["created_by"] = admin.id
    team_obj = Team(**team_dict)
    await db.teams.insert_one(team_obj.dict())
    return team_obj

@api_router.get("/teams", response_model=List[Team])
async def get_teams(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        teams = await db.teams.find().to_list(1000)
    else:
        teams = await db.teams.find({"id": current_user.team_id}).to_list(1000)
    return [Team(**team) for team in teams]

# Task Routes
@api_router.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user)):
    # Verify user can create task in this team
    if not current_user.is_admin and current_user.team_id != task.team_id:
        raise HTTPException(status_code=403, detail="Not authorized for this team")
    
    task_dict = task.dict()
    task_obj = Task(**task_dict)
    await db.tasks.insert_one(task_obj.dict())
    
    # Get responsible user for email notification
    responsible_user = await db.users.find_one({"id": task.responsible_user_id})
    if responsible_user:
        await send_notification_email(
            responsible_user["email"], 
            task.title, 
            task.description or ""
        )
    
    return task_obj

@api_router.get("/tasks", response_model=List[Task])
async def get_tasks(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        tasks = await db.tasks.find().to_list(1000)
    else:
        tasks = await db.tasks.find({"team_id": current_user.team_id}).to_list(1000)
    return [Task(**task) for task in tasks]

@api_router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, current_user: User = Depends(get_current_user)):
    task = await db.tasks.find_one({"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_obj = Task(**task)
    
    # Check permissions
    if not current_user.is_admin and current_user.team_id != task_obj.team_id:
        raise HTTPException(status_code=403, detail="Not authorized for this team")
    
    return task_obj

@api_router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate, current_user: User = Depends(get_current_user)):
    existing_task = await db.tasks.find_one({"id": task_id})
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    existing_task_obj = Task(**existing_task)
    
    # Check permissions
    if not current_user.is_admin and current_user.team_id != existing_task_obj.team_id:
        raise HTTPException(status_code=403, detail="Not authorized for this team")
    
    # Update task
    update_data = task_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db.tasks.update_one({"id": task_id}, {"$set": update_data})
    
    # Get updated task
    updated_task = await db.tasks.find_one({"id": task_id})
    return Task(**updated_task)

@api_router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, current_user: User = Depends(get_current_user)):
    existing_task = await db.tasks.find_one({"id": task_id})
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    existing_task_obj = Task(**existing_task)
    
    # Check permissions
    if not current_user.is_admin and current_user.team_id != existing_task_obj.team_id:
        raise HTTPException(status_code=403, detail="Not authorized for this team")
    
    await db.tasks.delete_one({"id": task_id})
    return {"message": "Task deleted successfully"}

# Dashboard Routes
@api_router.get("/dashboard/stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    # Filter based on user permissions
    if current_user.is_admin:
        task_filter = {}
    else:
        task_filter = {"team_id": current_user.team_id}
    
    # Get all tasks for the user's scope
    tasks = await db.tasks.find(task_filter).to_list(10000)
    
    # Calculate stats
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t["status"] == "concluida"])
    in_progress_tasks = len([t for t in tasks if t["status"] == "em_progresso"])
    pending_tasks = len([t for t in tasks if t["status"] == "pendente"])
    
    # Overdue tasks (deadline passed and not completed)
    now = datetime.utcnow()
    overdue_tasks = len([
        t for t in tasks 
        if t.get("deadline") and t["deadline"] < now 
        and t["status"] != "concluida"
    ])
    
    # Stats by urgency
    urgency_stats = {
        "critica": len([t for t in tasks if t["urgency"] == "critica"]),
        "alta": len([t for t in tasks if t["urgency"] == "alta"]),
        "media": len([t for t in tasks if t["urgency"] == "media"]),
        "baixa": len([t for t in tasks if t["urgency"] == "baixa"])
    }
    
    # Stats by category
    categories = {}
    for task in tasks:
        cat = task["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
        "urgency_stats": urgency_stats,
        "category_stats": categories
    }

# Comments Routes
@api_router.post("/comments", response_model=Comment)
async def create_comment(comment: CommentCreate, current_user: User = Depends(get_current_user)):
    # Verify task exists and user has access
    task = await db.tasks.find_one({"id": comment.task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_obj = Task(**task)
    if not current_user.is_admin and current_user.team_id != task_obj.team_id:
        raise HTTPException(status_code=403, detail="Not authorized for this team")
    
    comment_dict = comment.dict()
    comment_dict["user_id"] = current_user.id
    comment_obj = Comment(**comment_dict)
    await db.comments.insert_one(comment_obj.dict())
    return comment_obj

@api_router.get("/tasks/{task_id}/comments", response_model=List[Comment])
async def get_task_comments(task_id: str, current_user: User = Depends(get_current_user)):
    # Verify task exists and user has access
    task = await db.tasks.find_one({"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_obj = Task(**task)
    if not current_user.is_admin and current_user.team_id != task_obj.team_id:
        raise HTTPException(status_code=403, detail="Not authorized for this team")
    
    comments = await db.comments.find({"task_id": task_id}).to_list(1000)
    return [Comment(**comment) for comment in comments]

# Include the router in the main app
app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()