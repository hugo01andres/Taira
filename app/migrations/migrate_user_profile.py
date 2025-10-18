import sqlite3
import os
from app.core.config import settings

def migrate_user_profile():
    """Add company fields to the user table."""
    print("User Profile Migration")
    print("=" * 40)
    
    # Get database path from settings
    db_path = settings.database_url.replace("sqlite:///", "")
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("1️⃣ Connected to database.")
        print("2️⃣ Checking existing columns...")
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Check if company_name column exists
        if 'company_name' in columns:
            print("   OK: company_name column already exists")
        else:
            print("   Adding company_name column...")
            cursor.execute("ALTER TABLE user ADD COLUMN company_name TEXT")
            print("   OK: company_name column added")
        
        # Check if company_website column exists
        if 'company_website' in columns:
            print("   OK: company_website column already exists")
        else:
            print("   Adding company_website column...")
            cursor.execute("ALTER TABLE user ADD COLUMN company_website TEXT")
            print("   OK: company_website column added")
        
        # Commit the changes
        conn.commit()
        print("3️⃣ Database migration completed successfully!")
        
        # Verify the columns were added
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'company_name' in columns and 'company_website' in columns:
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
    print("\n4️⃣ Checking database schema...")
    
    db_path = settings.database_url.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"   Connected to {db_path}")
        cursor.execute("PRAGMA table_info(user)")
        print("   User table schema:")
        for column in cursor.fetchall():
            print(f"      - {column[1]} ({column[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ERROR: Error checking schema: {e}")
        return False

if __name__ == "__main__":
    print("User Profile Migration Tool")
    print("=" * 50)
    
    # Run migration
    success = migrate_user_profile()
    
    if success:
        # Check schema
        check_database_schema()
        print("\nMigration completed successfully!")
        print("Users can now set their company information in their profile.")
    else:
        print("\nMigration failed")
        print("Please check the error messages above")
