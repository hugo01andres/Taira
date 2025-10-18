#!/usr/bin/env python3
"""
Migration Status Checker for Taira Application

This script checks the current status of database migrations.
Run this from the project root: python app/migrations/check_migration_status.py
"""

import sys
import sqlite3
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import settings

def check_table_schema(table_name, expected_columns):
    """Check if a table has the expected columns."""
    db_path = settings.database_url.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        
        conn.close()
        
        missing_columns = []
        for expected_col in expected_columns:
            if expected_col not in columns:
                missing_columns.append(expected_col)
        
        return missing_columns, columns
        
    except Exception as e:
        print(f"❌ Error checking {table_name}: {e}")
        return None, []

def main():
    """Check migration status."""
    print("Taira Database Migration Status")
    print("=" * 50)
    
    # Expected columns for each table
    expected_schemas = {
        'user': ['id', 'email', 'hashed_password', 'is_active', 'created_at', 'company_name', 'company_website'],
        'lead': ['id', 'user_id', 'vacancy_id', 'ai_message', 'ai_generated', 'created_at', 'additional_instructions'],
        'company': ['id', 'name', 'website', 'created_at'],
        'vacancy': ['id', 'title', 'description', 'company_id', 'created_at']
    }
    
    print("Checking database schema...")
    print()
    
    all_good = True
    
    for table_name, expected_columns in expected_schemas.items():
        print(f"Checking {table_name} table:")
        
        missing_columns, current_columns = check_table_schema(table_name, expected_columns)
        
        if missing_columns is None:
            print(f"   ERROR: Could not check {table_name} table")
            all_good = False
        elif missing_columns:
            print(f"   WARNING: Missing columns: {', '.join(missing_columns)}")
            all_good = False
        else:
            print(f"   OK: All expected columns present")
        
        print(f"   Current columns: {', '.join(current_columns)}")
        print()
    
    print("=" * 50)
    if all_good:
        print("SUCCESS: Database schema is up to date!")
        print("All required columns are present.")
    else:
        print("WARNING: Database schema needs updates.")
        print("Run migrations: python app/migrations/run_migrations.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
