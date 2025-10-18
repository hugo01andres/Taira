#!/usr/bin/env python3
"""
Database migration script to add the ai_generated column to the lead table.
This script will update the existing database to include the new AI fields.
"""

import sqlite3
import os
from app.core.config import settings

def migrate_database():
    """Add ai_generated column to the lead table."""
    print("Database Migration")
    print("=" * 40)
    
    # Get database path from settings
    db_path = settings.database_url.replace("sqlite:///", "")
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    print(f"1️⃣ Connecting to database: {db_path}")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if ai_generated column already exists
        print("2️⃣ Checking existing columns...")
        cursor.execute("PRAGMA table_info(lead)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'ai_generated' in columns:
            print("   OK: ai_generated column already exists")
            conn.close()
            return True
        
        print("   ERROR: ai_generated column not found")
        print("3. Adding ai_generated column...")
        
        # Add the ai_generated column
        cursor.execute("ALTER TABLE lead ADD COLUMN ai_generated BOOLEAN DEFAULT 0")
        
        # Commit the changes
        conn.commit()
        print("   OK: ai_generated column added successfully")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(lead)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'ai_generated' in columns:
            print("   OK: Column verification successful")
        else:
            print("   ERROR: Column verification failed")
            return False
        
        conn.close()
        print("4. Database migration completed successfully!")
        return True
        
    except sqlite3.Error as e:
        print(f"   ERROR: Database error: {e}")
        return False
    except Exception as e:
        print(f"   ERROR: Unexpected error: {e}")
        return False

def check_database_schema():
    """Check the current database schema."""
    print("\n5. Checking database schema...")
    
    db_path = settings.database_url.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("PRAGMA table_info(lead)")
        columns = cursor.fetchall()
        
        print("   Lead table columns:")
        for column in columns:
            print(f"      - {column[1]} ({column[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ERROR: Error checking schema: {e}")
        return False

if __name__ == "__main__":
    print("Database Migration Tool")
    print("=" * 50)
    
    # Run migration
    success = migrate_database()
    
    if success:
        # Check schema
        check_database_schema()
        print("\nMigration completed successfully!")
        print("Database is ready for AI features")
    else:
        print("\nMigration failed")
        print("Please check the error messages above")
