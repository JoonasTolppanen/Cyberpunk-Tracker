# Database Schema Changes

## Summary of Changes

The following schema modifications were made to the database:

### 1. Users Table - Removed Email Field ✓
**Changed:** Removed `email` field from users table  
**Reason:** Login only requires username and password

**Before:**
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,        -- REMOVED
    password_hash TEXT NOT NULL,
    ...
);
```

**After:**
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    ...
);
```

### 2. Contacts Table - Added 'other' Option ✓
**Changed:** Added 'other' to contact_type CHECK constraint  
**Reason:** Support for additional contact types beyond friend/love/enemy

**Before:**
```sql
contact_type TEXT CHECK(contact_type IN ('friend', 'love', 'enemy'))
```

**After:**
```sql
contact_type TEXT CHECK(contact_type IN ('friend', 'love', 'enemy', 'other'))
```

### 3. Reputation Table - Renamed Field ✓
**Changed:** Renamed `faction_name` to `reputation_event`  
**Removed:** `reputation_events` field (redundant)  
**Reason:** More flexible text field for describing reputation events

**Before:**
```sql
CREATE TABLE reputation (
    ...
    reputation_score INTEGER DEFAULT 0,
    reputation_events TEXT,
    faction_name TEXT,
    notes TEXT,
    ...
);
```

**After:**
```sql
CREATE TABLE reputation (
    ...
    reputation_score INTEGER DEFAULT 0,
    reputation_event TEXT,
    notes TEXT,
    ...
);
```

### 4. Ammo Table - Changed Field Name ✓
**Changed:** Renamed `caliber` to `description`  
**Reason:** More flexible field for describing ammunition

**Before:**
```sql
CREATE TABLE ammo (
    ...
    ammo_type TEXT NOT NULL,
    caliber TEXT,
    quantity INTEGER DEFAULT 0,
    ...
);
```

**After:**
```sql
CREATE TABLE ammo (
    ...
    ammo_type TEXT NOT NULL,
    description TEXT,
    quantity INTEGER DEFAULT 0,
    ...
);
```

### 5. Items Table - Removed Weight Field ✓
**Changed:** Removed `weight` field  
**Reason:** Simplified item tracking

**Before:**
```sql
CREATE TABLE items (
    ...
    description TEXT,
    weight REAL DEFAULT 0,        -- REMOVED
    value INTEGER DEFAULT 0,
    ...
);
```

**After:**
```sql
CREATE TABLE items (
    ...
    description TEXT,
    value INTEGER DEFAULT 0,
    ...
);
```

### BONUS: Addictions Table - Fixed Field Name ✓
**Changed:** Fixed incorrect field name from `effect` to `severity`  
**Added:** CHECK constraint for severity levels  
**Reason:** Bug fix - severity makes more sense for addiction tracking

**Before:**
```sql
CREATE TABLE addictions (
    ...
    substance TEXT NOT NULL,
    effect TEXT NOT NULL,
    notes TEXT,
    ...
);
```

**After:**
```sql
CREATE TABLE addictions (
    ...
    substance TEXT NOT NULL,
    severity TEXT CHECK(severity IN ('mild', 'moderate', 'severe')),
    notes TEXT,
    ...
);
```

## Files Updated

### Core Database Files
1. ✓ `schema.sql` - Updated table definitions
2. ✓ `db_helper.py` - Updated create_user function signature and docstrings
3. ✓ `example_data.py` - Updated sample data to match new schema
4. ✓ `test_db.py` - Updated test cases

### Documentation Files
5. ✓ `queries.sql` - Updated example queries
6. ✓ `QUICKSTART.md` - Updated quick reference
7. ✓ `STRUCTURE.md` - Updated entity diagrams and field descriptions

### Files Not Requiring Changes
- `README.md` - No specific field references
- `SUMMARY.md` - No specific field references
- `init_db.py` - Schema-agnostic
- Main project `README.md` - No specific field references

## Testing Results

### All Tests Pass ✓

```
✓ Database initialization
✓ User creation (without email)
✓ Character creation
✓ Stats management
✓ Contact management (supports 'other' type)
✓ Cybernetics management
✓ Inventory management (without weight)
✓ Character updates
```

### Example Data Loads Successfully ✓

```
✓ 2 users created (without email)
✓ 2 characters created
✓ 5 items created (without weight)
✓ 4 contacts created (including all types)
✓ 2 ammo types created (with description)
✓ 1 reputation entry (with reputation_event)
✓ 1 addiction (with severity)
```

## Migration Notes

If you have an existing database with the old schema:

### Option 1: Fresh Start (Recommended for Development)
```bash
cd database
rm cyberpunk_tracker.db
python3 init_db.py
python3 example_data.py
```

### Option 2: Manual Migration (For Production Data)
```sql
-- Remove email from users (SQLite doesn't support DROP COLUMN easily)
-- Best to recreate the table

-- Add 'other' to contacts (no migration needed, just update CHECK)

-- Rename faction_name to reputation_event
ALTER TABLE reputation RENAME COLUMN faction_name TO reputation_event;

-- Rename caliber to description in ammo
ALTER TABLE ammo RENAME COLUMN caliber TO description;

-- Remove weight from items (recreate table)

-- Fix addictions severity field (recreate table)
```

**Note:** SQLite has limited ALTER TABLE support. For complex migrations, it's often easier to:
1. Export data to JSON/CSV
2. Drop and recreate tables
3. Re-import data

## Impact Assessment

### Breaking Changes
- ✗ Code using `create_user('user', 'email@x.com', 'hash')` will fail
- ✗ Queries selecting `email` from users will fail
- ✗ Queries selecting `faction_name` from reputation will fail  
- ✗ Queries selecting `caliber` from ammo will fail
- ✗ Queries selecting `weight` from items will fail

### Non-Breaking Changes
- ✓ Adding 'other' to contact_type is backwards compatible
- ✓ Existing 'friend', 'love', 'enemy' contacts still work

## Verification Commands

```bash
# Verify schema changes
sqlite3 cyberpunk_tracker.db "PRAGMA table_info(users);"
sqlite3 cyberpunk_tracker.db "PRAGMA table_info(contacts);"
sqlite3 cyberpunk_tracker.db "PRAGMA table_info(reputation);"
sqlite3 cyberpunk_tracker.db "PRAGMA table_info(ammo);"
sqlite3 cyberpunk_tracker.db "PRAGMA table_info(items);"

# Run tests
python3 test_db.py

# Load example data
python3 example_data.py
```

## Date
Changes made: January 29, 2026
