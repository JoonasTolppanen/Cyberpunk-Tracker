# Cyberpunk Tracker Database

SQLite database schema and utilities for the Cyberpunk Tracker project.

## Database Structure

### Tables

1. **users** - User accounts
   - User credentials and account information

2. **characters** - Character profiles (hahmot)
   - Basic character information, identifying features, status (HP, humanity, death saves)

3. **background** - Character backgrounds
   - Family background and childhood environment

4. **contacts** - Character relationships (contactit)
   - Friends, lovers, and enemies with detailed information

5. **status_effects** - Active status effects
   - Buffs, debuffs, and conditions affecting the character

6. **critical_injuries** - Critical injuries tracking
   - Permanent or healing injuries with descriptions

7. **addictions** - Character addictions
   - Substance addictions with severity levels

8. **reputation** - Character reputation
   - Reputation scores and events with different factions

9. **stats** - Character statistics
   - All core stats (Intelligence, Reflexes, Dexterity, etc.)

10. **items** - Item database
    - Master list of all items in the game

11. **inventory** - Character inventory
    - Links characters to items they own

12. **ammo** - Ammunition tracking
    - Different ammo types and quantities per character

13. **cybernetics** - Cybernetic implants
    - Implants installed on characters with humanity costs

14. **maps** - Game maps (kartat)
    - Districts, buildings, combat maps, etc.

15. **character_maps** - Character-map relationships
    - Links characters to relevant maps

## Setup

### 1. Initialize the Database

Run the initialization script to create the database:

```bash
cd database
python3 init_db.py
```

This will create `cyberpunk_tracker.db` with all tables.

### 2. Reset Database (Optional)

To delete the existing database and create a fresh one:

```bash
python3 init_db.py --reset
```

### 3. Custom Database Path

To create the database in a specific location:

```bash
python3 init_db.py /path/to/custom/database.db
```

## Usage

### Python Integration

Use the `DatabaseHelper` class for easy database operations:

```python
from database.db_helper import DatabaseHelper

# Initialize
db = DatabaseHelper('cyberpunk_tracker.db')

# Create a user
user_id = db.create_user('player1', 'player1@example.com', 'password_hash')

# Create a character
char_id = db.create_character(
    user_id=user_id,
    handle='V',
    role='Solo',
    hp=40,
    max_hp=40,
    humanity=50,
    max_humanity=50
)

# Set character stats
db.set_character_stats(
    char_id,
    intelligence=7,
    reflexes=8,
    dexterity=6,
    technique=5,
    cool=7,
    willpower=6,
    luck=5,
    movement=5,
    body=6,
    empathy=4
)

# Add a contact
db.add_contact(
    char_id,
    contact_type='friend',
    name='Jackie Welles',
    contact_number=1,
    notes='Best friend and partner'
)

# Add cybernetics
db.add_cybernetic(
    char_id,
    name='Mantis Blades',
    body_location='Arms',
    humanity_cost=7,
    description='Retractable blade implants'
)

# Get character info
character = db.get_character(char_id)
stats = db.get_character_stats(char_id)
contacts = db.get_character_contacts(char_id)
```

### Direct SQL Queries

You can also execute SQL queries directly:

```python
# Custom query
results = db.execute_query(
    "SELECT * FROM characters WHERE role = ?",
    ('Solo',)
)

# Update query
rows_affected = db.execute_update(
    "UPDATE characters SET hp = ? WHERE character_id = ?",
    (35, char_id)
)
```

## Schema Details

### Character Status Tracking

Characters track multiple status values:
- **HP (Health Points)**: Current and maximum health
- **Humanity**: Current and maximum humanity (affected by cybernetics)
- **Death Save**: Death save counter for critical damage
- **Critical Injuries**: Separate table for permanent injuries
- **Addictions**: Separate table for substance dependencies
- **Status Effects**: Temporary buffs/debuffs

### Inventory System

The inventory system uses a many-to-many relationship:
- **items** table: Master list of all possible items
- **inventory** table: Links characters to items they own
- Tracks quantity, equipped status, and notes per item

### Contact System

Contacts support three types:
- **friend**: Friends and allies
- **love**: Romantic interests
- **enemy**: Enemies with detailed tracking (who wronged whom, what happened, etc.)

Each contact has a `contact_number` field to track multiple contacts of the same type (e.g., Friend #1, Friend #2).

### Cybernetics System

Tracks installed cybernetic implants with:
- Body location
- Humanity cost
- Installation date
- Malfunction status
- Custom notes

## File Structure

```
database/
├── schema.sql           # Database schema definition
├── init_db.py          # Database initialization script
├── db_helper.py        # Helper functions for database operations
├── example_data.py     # Script to populate with sample data
└── README.md           # This file
```

## Notes

- The database uses SQLite, which is file-based and doesn't require a server
- All foreign keys use `ON DELETE CASCADE` to maintain referential integrity
- Timestamps use SQLite's `CURRENT_TIMESTAMP` for automatic date tracking
- Character stats follow the Cyberpunk RED stat system
- The schema is designed to integrate with the existing web-based interface

## Future Enhancements

Potential additions to consider:
- Skills table (separate from stats)
- Combat log/history
- Quest/mission tracking
- Experience points and leveling
- Money/currency tracking
- Vehicle/property ownership
- Session/game state management
