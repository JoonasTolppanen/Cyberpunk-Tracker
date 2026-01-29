# Quick Start Guide

Get your Cyberpunk Tracker database up and running in 5 minutes!

## Step 1: Initialize Database (30 seconds)

```bash
cd database
python3 init_db.py
```

Expected output:
```
✓ Database created successfully at: cyberpunk_tracker.db
✓ All tables initialized
```

## Step 2: Verify Installation (10 seconds)

```bash
python3 test_db.py
```

You should see all tests pass. If any fail, check the error message.

## Step 3: Add Example Data (20 seconds)

```bash
python3 example_data.py
```

This creates:
- 2 demo users
- 2 characters (V and Johnny Silverhand)
- Sample items, contacts, cybernetics, etc.

## Step 4: Try Some Queries

### Python Way

```python
from database.db_helper import DatabaseHelper

# Connect to database
db = DatabaseHelper('cyberpunk_tracker.db')

# Get all characters
chars = db.execute_query("SELECT handle, role, hp FROM characters")
for char in chars:
    print(f"{char['handle']} - {char['role']} (HP: {char['hp']})")
```

### SQL Way

```bash
sqlite3 cyberpunk_tracker.db
```

Then try these queries:

```sql
-- List all characters
SELECT handle, role, hp FROM characters;

-- Get character with stats
SELECT c.handle, s.intelligence, s.reflexes, s.cool
FROM characters c
JOIN stats s ON c.character_id = s.character_id;

-- Exit sqlite3
.quit
```

## Common Tasks

### Create a New Character

```python
from database.db_helper import DatabaseHelper

db = DatabaseHelper('cyberpunk_tracker.db')

# Create character
char_id = db.create_character(
    user_id=1,
    handle='YourCharacter',
    role='Netrunner',
    hp=30,
    max_hp=30,
    humanity=50,
    max_humanity=50
)

# Add stats
db.set_character_stats(
    char_id,
    intelligence=8,
    reflexes=6,
    cool=7,
    body=4
)

print(f"Created character with ID: {char_id}")
```

### Add Item to Inventory

```python
# First, create or find an item
item_id = db.execute_update(
    "INSERT INTO items (item_name, item_type, value) VALUES (?, ?, ?)",
    ('Cool Jacket', 'armor', 200)
)

# Add to character's inventory
db.add_item_to_inventory(char_id=1, item_id=item_id, quantity=1)
```

### Update Character HP

```python
# Take damage
db.update_character(1, hp=25)

# Or with SQL
db.execute_update("UPDATE characters SET hp = hp - 5 WHERE character_id = ?", (1,))
```

### Add a Contact

```python
db.add_contact(
    character_id=1,
    contact_type='friend',
    name='Rogue',
    contact_number=1,
    notes='Fixer at the Afterlife'
)
```

### Install Cybernetics

```python
db.add_cybernetic(
    character_id=1,
    name='Cyberoptics',
    body_location='Eyes',
    humanity_cost=3,
    description='Enhanced vision with zoom and thermal'
)
```

## File Structure

```
database/
├── cyberpunk_tracker.db    # Your actual database (created after init)
├── schema.sql              # Database structure definition
├── init_db.py              # Creates the database
├── db_helper.py            # Python helper functions
├── example_data.py         # Populate with sample data
├── test_db.py              # Run tests
├── queries.sql             # Common SQL queries reference
├── STRUCTURE.md            # Detailed schema documentation
├── QUICKSTART.md           # This file
└── README.md               # Full documentation
```

## Troubleshooting

### Database doesn't exist
```bash
python3 init_db.py
```

### Python module errors
Make sure you're in the database directory:
```bash
cd /path/to/Softa_2/database
```

### Want to start fresh
```bash
python3 init_db.py --reset
```
Then reload sample data:
```bash
python3 example_data.py
```

### Can't import db_helper
```python
# If running from project root
from database.db_helper import DatabaseHelper

# If running from database folder
from db_helper import DatabaseHelper
```

## Next Steps

1. **Read the documentation**: Check out `README.md` for detailed API docs
2. **Explore queries**: Look at `queries.sql` for query examples
3. **Understand structure**: Read `STRUCTURE.md` for database design
4. **Build your app**: Integrate with your web interface

## Integration with Web Interface

### Option 1: Backend API
Create a Flask/FastAPI backend that uses `db_helper.py`:

```python
from flask import Flask, jsonify
from database.db_helper import DatabaseHelper

app = Flask(__name__)
db = DatabaseHelper('database/cyberpunk_tracker.db')

@app.route('/character/<int:char_id>')
def get_character(char_id):
    char = db.get_character(char_id)
    stats = db.get_character_stats(char_id)
    return jsonify({'character': char, 'stats': stats})
```

### Option 2: Direct Browser
Use a library like sql.js to run SQLite in the browser:
- Load the database file
- Execute queries client-side
- No backend needed!

### Option 3: Hybrid
- Keep using localStorage for temporary data
- Sync to SQLite when "saving" to server
- Best of both worlds

## Tips & Best Practices

1. **Always use transactions** for multiple related updates
2. **Use parameterized queries** to prevent SQL injection
3. **Back up your database** regularly (it's just one file!)
4. **Don't store passwords in plain text** - use proper hashing
5. **Index frequently queried fields** for better performance

## Need Help?

- Check the error message - SQLite errors are usually clear
- Look at `example_data.py` for working examples
- Review `queries.sql` for query syntax
- Read `README.md` for detailed documentation

## Quick Reference

```python
from database.db_helper import DatabaseHelper
db = DatabaseHelper('cyberpunk_tracker.db')

# Users
user_id = db.create_user('username', 'hash')
user = db.get_user(user_id)

# Characters
char_id = db.create_character(user_id, 'Handle', role='Solo')
char = db.get_character(char_id)
db.update_character(char_id, hp=30)

# Stats
db.set_character_stats(char_id, intelligence=7, reflexes=8)
stats = db.get_character_stats(char_id)

# Inventory
db.add_item_to_inventory(char_id, item_id, quantity=1)
inventory = db.get_character_inventory(char_id)

# Contacts
db.add_contact(char_id, 'friend', 'Name')
contacts = db.get_character_contacts(char_id)

# Cybernetics
db.add_cybernetic(char_id, 'Name', 'Location', humanity_cost=5)
cybernetics = db.get_character_cybernetics(char_id)

# Custom queries
results = db.execute_query("SELECT * FROM characters WHERE role = ?", ('Solo',))
rows = db.execute_update("UPDATE characters SET hp = ? WHERE character_id = ?", (35, char_id))
```

That's it! You're ready to start using the Cyberpunk Tracker database. 🎮
