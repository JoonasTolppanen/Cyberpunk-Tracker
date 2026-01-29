#!/usr/bin/env python3
"""
Database initialization script for Cyberpunk Tracker
Creates the SQLite database and sets up all tables
"""

import sqlite3
import os

def init_database(db_path='cyberpunk_tracker.db'):
    """
    Initialize the database by executing the schema.sql file
    
    Args:
        db_path: Path where the database file will be created
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(script_dir, 'schema.sql')
    
    # Read the schema file
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find schema.sql at {schema_path}")
        return False
    
    # Create/connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute the schema
        cursor.executescript(schema_sql)
        
        conn.commit()
        print(f"✓ Database created successfully at: {db_path}")
        print(f"✓ All tables initialized")
        
        # Show created tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        print(f"\nCreated tables ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
        return False

def reset_database(db_path='cyberpunk_tracker.db'):
    """
    Delete existing database and create a fresh one
    
    Args:
        db_path: Path to the database file
    """
    if os.path.exists(db_path):
        response = input(f"Database '{db_path}' exists. Delete it? (yes/no): ")
        if response.lower() == 'yes':
            os.remove(db_path)
            print(f"✓ Deleted existing database")
        else:
            print("Aborted.")
            return False
    
    return init_database(db_path)

if __name__ == '__main__':
    import sys
    
    print("Cyberpunk Tracker - Database Initialization")
    print("=" * 50)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--reset':
            reset_database()
        else:
            db_path = sys.argv[1]
            init_database(db_path)
    else:
        init_database()
