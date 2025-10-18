#!/usr/bin/env python3
"""
Migration Runner for Taira Application

This script runs all database migrations in the correct order.
Run this from the project root: python app/migrations/run_migrations.py
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def run_migration(module_name, description):
    """Run a specific migration module."""
    print(f"\n{'='*60}")
    print(f"Running Migration: {description}")
    print(f"{'='*60}")
    
    try:
        # Import and run the migration
        module = __import__(f"app.migrations.{module_name}", fromlist=[module_name])
        
        # Look for the main migration function
        if hasattr(module, 'migrate_database'):
            success = module.migrate_database()
        elif hasattr(module, 'migrate_user_profile'):
            success = module.migrate_user_profile()
        elif hasattr(module, 'migrate_lead_instructions'):
            success = module.migrate_lead_instructions()
        else:
            print(f"❌ No migration function found in {module_name}")
            return False
            
        if success:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    """Run all migrations in order."""
    print("Taira Database Migrations")
    print("=" * 60)
    print("This will run all database migrations in the correct order.")
    print("Make sure you have backed up your database before proceeding.")
    
    # List of migrations in order
    migrations = [
        ("migrate_database", "Add ai_generated column to lead table"),
        ("migrate_user_profile", "Add company fields to user table"),
        ("migrate_lead_instructions", "Add additional_instructions field to lead table"),
    ]
    
    print(f"\nFound {len(migrations)} migrations to run:")
    for i, (module, desc) in enumerate(migrations, 1):
        print(f"  {i}. {desc}")
    
    # Ask for confirmation
    response = input("\nDo you want to proceed? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Migration cancelled.")
        return
    
    print("\nStarting migrations...")
    
    # Run each migration
    all_success = True
    for module_name, description in migrations:
        success = run_migration(module_name, description)
        if not success:
            all_success = False
            print(f"\n❌ Migration failed: {description}")
            print("Stopping migration process.")
            break
    
    # Final result
    print(f"\n{'='*60}")
    if all_success:
        print("🎉 All migrations completed successfully!")
        print("Your database is now up to date.")
    else:
        print("❌ Some migrations failed.")
        print("Please check the error messages above and fix any issues.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
