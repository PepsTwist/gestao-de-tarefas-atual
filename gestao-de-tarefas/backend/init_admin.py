#!/usr/bin/env python3
"""
Script to create initial admin user and sample data
"""
import asyncio
import uuid
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_admin_user():
    """Create initial admin user"""
    admin_email = "admin@taskmanager.com"
    admin_password = "admin123"
    
    # Check if admin already exists
    existing_admin = await db.users.find_one({"email": admin_email})
    if existing_admin:
        print(f"Admin user {admin_email} already exists")
        return existing_admin["id"]
    
    # Create admin user
    admin_user = {
        "id": str(uuid.uuid4()),
        "email": admin_email,
        "name": "Administrador",
        "password_hash": get_password_hash(admin_password),
        "is_admin": True,
        "team_id": None,
        "created_at": datetime.utcnow()
    }
    
    await db.users.insert_one(admin_user)
    print(f"Created admin user: {admin_email} / password: {admin_password}")
    return admin_user["id"]

async def create_sample_team(admin_id):
    """Create sample team"""
    team_name = "Equipe Desenvolvimento"
    
    # Check if team already exists
    existing_team = await db.teams.find_one({"name": team_name})
    if existing_team:
        print(f"Team {team_name} already exists")
        return existing_team["id"]
    
    team = {
        "id": str(uuid.uuid4()),
        "name": team_name,
        "description": "Equipe responsável pelo desenvolvimento de software",
        "created_by": admin_id,
        "created_at": datetime.utcnow()
    }
    
    await db.teams.insert_one(team)
    print(f"Created team: {team_name}")
    return team["id"]

async def create_sample_users(team_id):
    """Create sample users"""
    users = [
        {
            "email": "joao@taskmanager.com",
            "name": "João Silva",
            "password": "user123"
        },
        {
            "email": "maria@taskmanager.com", 
            "name": "Maria Santos",
            "password": "user123"
        },
        {
            "email": "pedro@taskmanager.com",
            "name": "Pedro Oliveira", 
            "password": "user123"
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data["email"]})
        if existing_user:
            print(f"User {user_data['email']} already exists")
            created_users.append(existing_user["id"])
            continue
        
        user = {
            "id": str(uuid.uuid4()),
            "email": user_data["email"],
            "name": user_data["name"],
            "password_hash": get_password_hash(user_data["password"]),
            "is_admin": False,
            "team_id": team_id,
            "created_at": datetime.utcnow()
        }
        
        await db.users.insert_one(user)
        print(f"Created user: {user_data['email']} / password: {user_data['password']}")
        created_users.append(user["id"])
    
    return created_users

async def create_sample_tasks(team_id, user_ids, admin_id):
    """Create sample tasks"""
    tasks = [
        {
            "title": "Implementar sistema de login",
            "description": "Desenvolver a funcionalidade de autenticação de usuários",
            "category": "Desenvolvimento",
            "urgency": "alta"
        },
        {
            "title": "Criar dashboard administrativo",
            "description": "Desenvolver interface para administradores gerenciarem o sistema",
            "category": "Frontend",
            "urgency": "media"
        },
        {
            "title": "Configurar banco de dados",
            "description": "Configurar e otimizar a estrutura do banco MongoDB",
            "category": "Backend",
            "urgency": "critica"
        },
        {
            "title": "Testes de integração",
            "description": "Implementar testes automatizados para as APIs",
            "category": "QA",
            "urgency": "baixa"
        }
    ]
    
    statuses = ["pendente", "em_progresso", "concluida"]
    
    for i, task_data in enumerate(tasks):
        task = {
            "id": str(uuid.uuid4()),
            "title": task_data["title"],
            "description": task_data["description"],
            "responsible_user_id": user_ids[i % len(user_ids)],
            "deadline": None,
            "category": task_data["category"],
            "urgency": task_data["urgency"],
            "status": statuses[i % len(statuses)],
            "requested_by": admin_id,
            "team_id": team_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await db.tasks.insert_one(task)
        print(f"Created task: {task_data['title']}")

async def main():
    print("Initializing TaskManager database with sample data...")
    
    # Create admin user
    admin_id = await create_admin_user()
    
    # Create sample team
    team_id = await create_sample_team(admin_id)
    
    # Create sample users
    user_ids = await create_sample_users(team_id)
    
    # Create sample tasks
    await create_sample_tasks(team_id, user_ids, admin_id)
    
    print("\nDatabase initialization complete!")
    print("\nLogin credentials:")
    print("Admin: admin@taskmanager.com / admin123")
    print("Users: joao@taskmanager.com / user123")
    print("       maria@taskmanager.com / user123")
    print("       pedro@taskmanager.com / user123")
    
    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(main())