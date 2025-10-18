#!/usr/bin/env python3
"""
Check database content to see if sensitive data was committed.
"""

import sqlite3
import sys

def check_database_content():
    """Check what's in the committed database."""
    print("🔍 Checking Database Content")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect('taira.db')
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables found: {[t[0] for t in tables]}")
        
        # Check each table for data
        for table_name in [t[0] for t in tables]:
            print(f"\n📋 Table: {table_name}")
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   Records: {count}")
            
            if count > 0:
                # Show sample data (first 3 rows)
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                rows = cursor.fetchall()
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                print(f"   Columns: {columns}")
                
                print("   Sample data:")
                for i, row in enumerate(rows):
                    print(f"     Row {i+1}: {row}")
        
        conn.close()
        
        # Security assessment
        print("\n" + "=" * 40)
        print("🔒 SECURITY ASSESSMENT")
        print("=" * 40)
        
        # Check for sensitive data
        conn = sqlite3.connect('taira.db')
        cursor = conn.cursor()
        
        # Check for user data
        try:
            cursor.execute("SELECT COUNT(*) FROM user")
            user_count = cursor.fetchone()[0]
            if user_count > 0:
                print("⚠️  WARNING: User data found in database!")
                cursor.execute("SELECT email, is_active FROM user LIMIT 5")
                users = cursor.fetchall()
                print("   User emails found:")
                for email, active in users:
                    print(f"     - {email} (active: {active})")
            else:
                print("✅ No user data found")
        except:
            print("✅ No user table or data found")
        
        # Check for company data
        try:
            cursor.execute("SELECT COUNT(*) FROM company")
            company_count = cursor.fetchone()[0]
            if company_count > 0:
                print("⚠️  WARNING: Company data found in database!")
                cursor.execute("SELECT name, website FROM company LIMIT 5")
                companies = cursor.fetchall()
                print("   Companies found:")
                for name, website in companies:
                    print(f"     - {name} ({website})")
            else:
                print("✅ No company data found")
        except:
            print("✅ No company table or data found")
        
        # Check for lead data
        try:
            cursor.execute("SELECT COUNT(*) FROM lead")
            lead_count = cursor.fetchone()[0]
            if lead_count > 0:
                print("⚠️  WARNING: Lead data found in database!")
                cursor.execute("SELECT ai_message FROM lead WHERE ai_message IS NOT NULL LIMIT 3")
                leads = cursor.fetchall()
                if leads:
                    print("   AI messages found:")
                    for msg in leads:
                        print(f"     - {msg[0][:50]}...")
            else:
                print("✅ No lead data found")
        except:
            print("✅ No lead table or data found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    check_database_content()
