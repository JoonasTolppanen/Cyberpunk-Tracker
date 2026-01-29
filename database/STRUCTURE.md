# Database Structure Overview

## Entity Relationship Diagram (Text Format)

```
┌─────────────────┐
│     users       │
│─────────────────│
│ user_id (PK)    │
│ username        │
│ password_hash   │
│ created_at      │
│ last_login      │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│   characters    │◄──────────────┐
│─────────────────│               │
│ character_id(PK)│               │
│ user_id (FK)    │               │
│ handle          │               │
│ role            │               │
│ hp, max_hp      │               │
│ humanity        │               │
│ death_save      │               │
│ ...             │               │
└─────────────────┘               │
         │                        │
         │ 1:1                    │
         ├──────────┐             │
         │          │             │
         ▼          ▼             │
┌──────────┐  ┌─────────┐        │
│background│  │  stats  │        │
│──────────│  │─────────│        │
│bg_id (PK)│  │stat_id  │        │
│char_id   │  │char_id  │        │
│family... │  │intel.   │        │
│childhood │  │reflexes │        │
└──────────┘  │dex...   │        │
              └─────────┘        │
                                 │
         ┌───────────────────────┤
         │                       │
         │ 1:N                   │
         ▼                       │
┌─────────────────┐              │
│    contacts     │              │
│─────────────────│              │
│ contact_id (PK) │              │
│ character_id(FK)│              │
│ contact_type    │              │
│ name            │              │
│ notes           │              │
│ ...enemy fields │              │
└─────────────────┘              │
                                 │
         ┌───────────────────────┤
         │                       │
         │ 1:N                   │
         ▼                       │
┌─────────────────┐              │
│  cybernetics    │              │
│─────────────────│              │
│ cybernetic_id   │              │
│ character_id(FK)│              │
│ name            │              │
│ body_location   │              │
│ humanity_cost   │              │
│ malfunction     │              │
└─────────────────┘              │
                                 │
         ┌───────────────────────┤
         │                       │
         │ 1:N                   │
         ▼                       │
┌─────────────────┐              │
│ status_effects  │              │
│─────────────────│              │
│ effect_id (PK)  │              │
│ character_id(FK)│              │
│ effect_name     │              │
│ effect_type     │              │
│ active          │              │
└─────────────────┘              │
                                 │
         ┌───────────────────────┤
         │                       │
         │ 1:N                   │
         ▼                       │
┌─────────────────┐              │
│critical_injuries│              │
│─────────────────│              │
│ injury_id (PK)  │              │
│ character_id(FK)│              │
│ injury_name     │              │
│ description     │              │
│ healed          │              │
└─────────────────┘              │
                                 │
         ┌───────────────────────┤
         │                       │
         │ 1:N                   │
         ▼                       │
┌─────────────────┐              │
│   addictions    │              │
│─────────────────│              │
│ addiction_id    │              │
│ character_id(FK)│              │
│ substance       │              │
│ severity        │              │
└─────────────────┘              │
                                 │
         ┌───────────────────────┤
         │                       │
         │ 1:N                   │
         ▼                       │
┌─────────────────┐              │
│   reputation    │              │
│─────────────────│              │
│ reputation_id   │              │
│ character_id(FK)│              │
│ reputation_event│              │
│ reputation_score│              │
└─────────────────┘              │
                                 │
         ┌───────────────────────┤
         │                       │
         │ 1:N                   │
         ▼                       │
┌─────────────────┐              │
│      ammo       │              │
│─────────────────│              │
│ ammo_id (PK)    │              │
│ character_id(FK)│              │
│ ammo_type       │              │
│ description     │              │
│ quantity        │              │
└─────────────────┘              │
                                 │
                                 │
┌─────────────────┐              │
│     items       │              │
│─────────────────│              │
│ item_id (PK)    │              │
│ item_name       │              │
│ item_type       │              │
│ description     │              │
│ value           │              │
│ damage          │              │
│ armor_value     │              │
└─────────────────┘              │
         │                       │
         │ N:M                   │
         ▼                       │
┌─────────────────┐              │
│   inventory     │              │
│─────────────────│              │
│ inventory_id(PK)│              │
│ character_id(FK)├──────────────┘
│ item_id (FK)    │
│ quantity        │
│ equipped        │
└─────────────────┘

┌─────────────────┐
│      maps       │
│─────────────────│
│ map_id (PK)     │
│ map_name        │
│ map_type        │
│ image_path      │
│ data (JSON)     │
└─────────────────┘
         │
         │ N:M
         ▼
┌─────────────────┐
│ character_maps  │
│─────────────────│
│ character_id(FK)│───────┐
│ map_id (FK)     │       │
│ notes           │       │
└─────────────────┘       │
                          │
              ┌───────────┘
              │
              ▼
      (back to characters)
```

## Table Relationships

### One-to-Many (1:N)
- **users → characters**: One user can have multiple characters
- **characters → background**: One character has one background
- **characters → stats**: One character has one stats record
- **characters → contacts**: One character can have multiple contacts
- **characters → status_effects**: One character can have multiple effects
- **characters → critical_injuries**: One character can have multiple injuries
- **characters → addictions**: One character can have multiple addictions
- **characters → reputation**: One character can have multiple reputation entries
- **characters → ammo**: One character can have multiple ammo types
- **characters → cybernetics**: One character can have multiple cybernetics

### Many-to-Many (N:M)
- **characters ↔ items**: Via `inventory` junction table
  - One character can have many items
  - One item can be owned by many characters
  
- **characters ↔ maps**: Via `character_maps` junction table
  - One character can be associated with many maps
  - One map can be relevant to many characters

## Cascade Behavior

All foreign keys use `ON DELETE CASCADE`, meaning:

- Deleting a **user** will delete all their **characters**
- Deleting a **character** will delete:
  - Their background
  - Their stats
  - All contacts
  - All status effects
  - All critical injuries
  - All addictions
  - All reputation entries
  - All ammo records
  - All cybernetics
  - All inventory entries
  - All character-map associations

- Deleting an **item** will remove it from all inventories
- Deleting a **map** will remove all character associations

## Key Design Decisions

### Character Status Tracking
Multiple tables track different aspects of character health/status:
- **characters.hp, humanity**: Core tracked values
- **status_effects**: Temporary conditions (buffs/debuffs)
- **critical_injuries**: Permanent or long-term damage
- **addictions**: Substance dependencies

This separation allows for:
- Easier filtering (e.g., "show only active effects")
- Historical tracking (e.g., "healed injuries")
- Specific queries for each type

### Contact Types
The `contacts` table uses a single type field with three values:
- `friend`
- `love`
- `enemy`

Enemy contacts have additional fields:
- `who_wronged`, `what_caused`, `what_throw_down`, `what_happened`

These fields are NULL for friends and lovers.

### Inventory System
Separation of `items` and `inventory` allows:
- **items**: Master database of all possible items
- **inventory**: What each character actually owns
- Same item can be owned by multiple characters
- Item properties (damage, value) defined once
- Character-specific data (quantity, equipped) in inventory

### Stats Structure
All core Cyberpunk RED stats in one table:
- Intelligence, Reflexes, Dexterity, Technique
- Cool, Willpower, Luck, Movement, Body, Empathy

One row per character, making queries simple.

### Maps with JSON Data
Maps store flexible data in JSON format:
- Markers, zones, notes
- Can be parsed/updated without schema changes
- Allows for future expansion

## Indexing Strategy

Indexes are created on:
- `characters.user_id` - Fast user character lookup
- `inventory.character_id` - Fast inventory queries
- `stats.character_id` - Fast stats lookup
- `contacts.character_id` - Fast contact queries
- `cybernetics.character_id` - Fast cybernetics queries

Primary keys are automatically indexed by SQLite.

## Data Types

### SQLite Type Mappings
- `INTEGER`: Whole numbers, auto-increment for PRIMARY KEY
- `TEXT`: Variable-length strings (UTF-8)
- `REAL`: Floating-point numbers
- `BOOLEAN`: Stored as INTEGER (0 or 1)
- `TIMESTAMP`: Stored as TEXT in ISO 8601 format

### Constraints
- `NOT NULL`: Field must have a value
- `UNIQUE`: No duplicates allowed
- `CHECK`: Value must satisfy condition (e.g., contact_type)
- `DEFAULT`: Automatic value if not specified
- `FOREIGN KEY`: Referential integrity

## Common Query Patterns

### Get Complete Character
```sql
-- One query to get character with stats and background
SELECT c.*, s.*, b.*
FROM characters c
LEFT JOIN stats s ON c.character_id = s.character_id
LEFT JOIN background b ON c.character_id = b.character_id
WHERE c.character_id = ?
```

### Get Character Inventory
```sql
-- Join through inventory to get items
SELECT i.*, inv.quantity, inv.equipped
FROM inventory inv
JOIN items i ON inv.item_id = i.item_id
WHERE inv.character_id = ?
```

### Calculate Humanity Loss
```sql
-- Sum up cybernetic costs
SELECT c.humanity, SUM(cy.humanity_cost) as lost
FROM characters c
LEFT JOIN cybernetics cy ON c.character_id = cy.character_id
WHERE c.character_id = ?
GROUP BY c.character_id
```

## Normalization Level

The database follows **Third Normal Form (3NF)**:
- ✓ All fields depend on the primary key
- ✓ No repeating groups (contacts in separate table, not fields 1-4)
- ✓ No transitive dependencies
- ✓ Minimal data redundancy

### Example of Normalization
Instead of:
```
characters: friend1, friend2, friend3, friend4, enemy1, enemy2...
```

We use:
```
contacts: character_id, type, name, contact_number
```

This allows unlimited contacts of each type without schema changes.
