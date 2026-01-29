"""
Database helper functions for Cyberpunk Tracker
Provides convenience functions for common database operations
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

class DatabaseHelper:
    """Helper class for database operations"""
    
    def __init__(self, db_path='cyberpunk_tracker.db'):
        """
        Initialize the database helper
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """
        Execute a SELECT query and return results as list of dictionaries
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of dictionaries with query results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Last row ID for INSERT, or number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid if query.strip().upper().startswith('INSERT') else cursor.rowcount
    
    # ==================== User Operations ====================
    
    def create_user(self, username: str, password_hash: str) -> int:
        """Create a new user"""
        query = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        return self.execute_update(query, (username, password_hash))
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = ?"
        results = self.execute_query(query, (user_id,))
        return results[0] if results else None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = ?"
        results = self.execute_query(query, (username,))
        return results[0] if results else None
    
    # ==================== Character Operations ====================
    
    def create_character(self, user_id: int, handle: str, **kwargs) -> int:
        """Create a new character"""
        fields = ['user_id', 'handle']
        values = [user_id, handle]
        
        for key, value in kwargs.items():
            fields.append(key)
            values.append(value)
        
        placeholders = ', '.join(['?'] * len(values))
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO characters ({field_names}) VALUES ({placeholders})"
        return self.execute_update(query, tuple(values))
    
    def get_character(self, character_id: int) -> Optional[Dict]:
        """Get character by ID"""
        query = "SELECT * FROM characters WHERE character_id = ?"
        results = self.execute_query(query, (character_id,))
        return results[0] if results else None
    
    def get_user_characters(self, user_id: int) -> List[Dict]:
        """Get all characters for a user"""
        query = "SELECT * FROM characters WHERE user_id = ? ORDER BY created_date DESC"
        return self.execute_query(query, (user_id,))
    
    def update_character(self, character_id: int, **kwargs) -> int:
        """Update character fields"""
        if not kwargs:
            return 0
        
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [character_id]
        
        query = f"UPDATE characters SET {set_clause}, last_modified = CURRENT_TIMESTAMP WHERE character_id = ?"
        return self.execute_update(query, tuple(values))
    
    # ==================== Inventory Operations ====================
    
    def add_item_to_inventory(self, character_id: int, item_id: int, quantity: int = 1) -> int:
        """Add an item to character's inventory"""
        query = "INSERT INTO inventory (character_id, item_id, quantity) VALUES (?, ?, ?)"
        return self.execute_update(query, (character_id, item_id, quantity))
    
    def get_character_inventory(self, character_id: int) -> List[Dict]:
        """Get all items in character's inventory"""
        query = """
            SELECT i.*, inv.quantity, inv.equipped, inv.notes as inv_notes
            FROM inventory inv
            JOIN items i ON inv.item_id = i.item_id
            WHERE inv.character_id = ?
            ORDER BY i.item_type, i.item_name
        """
        return self.execute_query(query, (character_id,))
    
    def update_inventory_quantity(self, character_id: int, item_id: int, quantity: int) -> int:
        """Update quantity of an item in inventory"""
        query = "UPDATE inventory SET quantity = ? WHERE character_id = ? AND item_id = ?"
        return self.execute_update(query, (quantity, character_id, item_id))
    
    # ==================== Stats Operations ====================
    
    def set_character_stats(self, character_id: int, **stats) -> int:
        """Set character stats (creates or updates)"""
        # Check if stats exist
        existing = self.execute_query("SELECT stat_id FROM stats WHERE character_id = ?", (character_id,))
        
        if existing:
            # Update existing stats
            set_clause = ', '.join([f"{key} = ?" for key in stats.keys()])
            values = list(stats.values()) + [character_id]
            query = f"UPDATE stats SET {set_clause} WHERE character_id = ?"
            return self.execute_update(query, tuple(values))
        else:
            # Create new stats
            fields = ['character_id'] + list(stats.keys())
            values = [character_id] + list(stats.values())
            placeholders = ', '.join(['?'] * len(values))
            field_names = ', '.join(fields)
            query = f"INSERT INTO stats ({field_names}) VALUES ({placeholders})"
            return self.execute_update(query, tuple(values))
    
    def get_character_stats(self, character_id: int) -> Optional[Dict]:
        """Get character stats"""
        query = "SELECT * FROM stats WHERE character_id = ?"
        results = self.execute_query(query, (character_id,))
        return results[0] if results else None
    
    # ==================== Contacts Operations ====================
    
    def add_contact(self, character_id: int, contact_type: str, name: str, **kwargs) -> int:
        """Add a contact (friend, love, enemy, or other)"""
        fields = ['character_id', 'contact_type', 'name']
        values = [character_id, contact_type, name]
        
        for key, value in kwargs.items():
            fields.append(key)
            values.append(value)
        
        placeholders = ', '.join(['?'] * len(values))
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO contacts ({field_names}) VALUES ({placeholders})"
        return self.execute_update(query, tuple(values))
    
    def get_character_contacts(self, character_id: int, contact_type: Optional[str] = None) -> List[Dict]:
        """Get character's contacts, optionally filtered by type"""
        if contact_type:
            query = "SELECT * FROM contacts WHERE character_id = ? AND contact_type = ? ORDER BY contact_number"
            return self.execute_query(query, (character_id, contact_type))
        else:
            query = "SELECT * FROM contacts WHERE character_id = ? ORDER BY contact_type, contact_number"
            return self.execute_query(query, (character_id,))
    
    # ==================== Cybernetics Operations ====================
    
    def add_cybernetic(self, character_id: int, name: str, body_location: str, 
                      humanity_cost: int = 0, **kwargs) -> int:
        """Add a cybernetic implant"""
        fields = ['character_id', 'cybernetic_name', 'body_location', 'humanity_cost']
        values = [character_id, name, body_location, humanity_cost]
        
        for key, value in kwargs.items():
            fields.append(key)
            values.append(value)
        
        placeholders = ', '.join(['?'] * len(values))
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO cybernetics ({field_names}) VALUES ({placeholders})"
        return self.execute_update(query, tuple(values))
    
    def get_character_cybernetics(self, character_id: int) -> List[Dict]:
        """Get all cybernetics for a character"""
        query = "SELECT * FROM cybernetics WHERE character_id = ? ORDER BY installed_date"
        return self.execute_query(query, (character_id,))
    
    # ==================== Utility Functions ====================
    
    def delete_character(self, character_id: int) -> int:
        """Delete a character (cascades to related tables)"""
        query = "DELETE FROM characters WHERE character_id = ?"
        return self.execute_update(query, (character_id,))
    
    def get_table_count(self, table_name: str) -> int:
        """Get the number of rows in a table"""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0


# Example usage
if __name__ == '__main__':
    # Initialize the helper
    db = DatabaseHelper()
    
    # Example: Create a user
    # user_id = db.create_user('player1', 'hashed_password_here')
    # print(f"Created user with ID: {user_id}")
    
    # Example: Create a character
    # char_id = db.create_character(user_id, 'V', role='Solo', hp=40, max_hp=40)
    # print(f"Created character with ID: {char_id}")
    
    # Example: Set character stats
    # db.set_character_stats(char_id, intelligence=7, reflexes=8, cool=6, body=5)
    
    # Example: Get character info
    # character = db.get_character(char_id)
    # print(f"Character: {character}")
    
    print("Database helper loaded. Import this module to use the DatabaseHelper class.")
