#!/usr/bin/env python3
"""
Simple script to clear the database.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.database import engine
    from app.models.user import User
    from sqlmodel import Session, select
    
    print("Connecting to database...")
    
    with Session(engine) as session:
        # Get all users
        users = session.exec(select(User)).all()
        print(f"Found {len(users)} user(s) in database:")
        
        for user in users:
            print(f"- {user.email} (ID: {user.id})")
        
        if users:
            # Delete all users
            for user in users:
                session.delete(user)
            session.commit()
            print("✅ All users deleted from database!")
        else:
            print("✅ Database is already empty!")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the virtual environment and all dependencies are installed.")
except Exception as e:
    print(f"❌ Error: {e}")

print("\nNow you can register a new user without conflicts!")
