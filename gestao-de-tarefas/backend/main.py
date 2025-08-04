#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set up environment
os.environ.setdefault('PYTHONPATH', str(current_dir))

# Import the FastAPI app from server.py
try:
    from server import app
    # Export the app for Vercel
    application = app
    
    # Also make it available as handler for Vercel
    def handler(request, response):
        return app(request, response)
        
except ImportError as import_error:
    print(f"Error importing server: {import_error}")
    # Create a minimal fallback app
    from fastapi import FastAPI
    app = FastAPI()
    application = app
    
    @app.get("/")
    async def root():
        return {"error": "Server import failed", "message": str(import_error)}

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)