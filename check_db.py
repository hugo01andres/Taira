#!/usr/bin/env python3
"""
Script to check and optionally clear the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, init_db
from app.models.user import User
from sqlmodel import Session, select

def check_database():
    """Check what users are in the database."""
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        
        print("Users in database:")
        if users:
            for user in users:
                print(f"- ID: {user.id}, Email: {user.email}, Created: {user.created_at}")
        else:
            print("- No users found")
        
        return users

def clear_database():
    """Clear all users from the database."""
    with Session(engine) as session:
        # Delete all users
        session.exec(select(User)).all()
        for user in session.exec(select(User)):
            session.delete(user)
        session.commit()
        print("Database cleared!")

if __name__ == "__main__":
    print("Checking database...")
    users = check_database()
    
    if users:
        print(f"\nFound {len(users)} user(s).")
        response = input("Do you want to clear the database? (y/N): ")
        if response.lower() == 'y':
            clear_database()
            print("Database cleared. You can now register a new user.")
    else:
        print("Database is empty. You can register a new user.")
