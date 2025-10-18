import sqlite3

try:
    conn = sqlite3.connect('taira.db')
    cursor = conn.cursor()
    
    # Get tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables:", tables)
    
    # Check for data in each table
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} records")
        
        if count > 0:
            cursor.execute(f"SELECT * FROM {table} LIMIT 2")
            rows = cursor.fetchall()
            print(f"  Sample data: {rows}")
    
    conn.close()
    
except Exception as e:
    print("Error:", e)
