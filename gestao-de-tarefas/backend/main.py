#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent  
sys.path.insert(0, str(current_dir))

# Import the FastAPI app from server.py
from server import app

# For Vercel deployment - use Mangum adapter
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    # Fallback if Mangum is not available
    def handler(event, context):
        return {"statusCode": 500, "body": "Mangum adapter not available"}

# For compatibility
application = app

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
