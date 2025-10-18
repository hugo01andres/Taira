import sqlite3
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import settings

def migrate_lead_instructions():
    """Add additional_instructions field to the lead table."""
    print("Lead Instructions Migration")
    print("=" * 40)
    
    # Get database path from settings
    db_path = settings.database_url.replace("sqlite:///", "")
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("1. Connected to database.")
        print("2. Checking existing columns...")
        cursor.execute("PRAGMA table_info(lead)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Check if additional_instructions column exists
        if 'additional_instructions' in columns:
            print("   OK: additional_instructions column already exists")
        else:
            print("   Adding additional_instructions column...")
            cursor.execute("ALTER TABLE lead ADD COLUMN additional_instructions TEXT")
            print("   OK: additional_instructions column added")
        
        # Commit the changes
        conn.commit()
        print("3. Database migration completed successfully!")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(lead)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'additional_instructions' in columns:
            print("   OK: Column verification successful")
        else:
            print("   ERROR: Column verification failed")
            return False
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"   ERROR: Database error: {e}")
        return False
    except Exception as e:
        print(f"   ERROR: Unexpected error: {e}")
        return False

def check_database_schema():
    """Check the current database schema."""
    print("\n4. Checking database schema...")
    
    db_path = settings.database_url.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"   Connected to {db_path}")
        cursor.execute("PRAGMA table_info(lead)")
        print("   Lead table schema:")
        for column in cursor.fetchall():
            print(f"      - {column[1]} ({column[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ERROR: Error checking schema: {e}")
        return False

if __name__ == "__main__":
    print("Lead Instructions Migration Tool")
    print("=" * 50)
    
    # Run migration
    success = migrate_lead_instructions()
    
    if success:
        # Check schema
        check_database_schema()
        print("\nMigration completed successfully!")
        print("Users can now add custom instructions for AI message generation.")
    else:
        print("\nMigration failed")
        print("Please check the error messages above")
