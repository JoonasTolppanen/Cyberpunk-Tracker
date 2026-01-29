-- Cyberpunk Tracker Database Schema
-- SQLite Database

-- User accounts table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Characters table (hahmot)
CREATE TABLE IF NOT EXISTS characters (
    character_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    handle TEXT NOT NULL,
    role TEXT,
    role_ability TEXT,
    rank INTEGER DEFAULT 0,
    ability TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Identifying features
    cultural_region TEXT,
    clothing_style TEXT,
    hairstyle TEXT,
    affectation TEXT,
    languages TEXT,
    
    -- Status
    hp INTEGER DEFAULT 0,
    max_hp INTEGER DEFAULT 0,
    humanity INTEGER DEFAULT 0,
    max_humanity INTEGER DEFAULT 0,
    death_save INTEGER DEFAULT 0,
    
    -- Additional info
    improvement_points INTEGER DEFAULT 0,
    notes TEXT,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Background table
CREATE TABLE IF NOT EXISTS background (
    background_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    family_background TEXT,
    childhood_environment TEXT,
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Contacts table (contactit)
CREATE TABLE IF NOT EXISTS contacts (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    contact_type TEXT CHECK(contact_type IN ('friend', 'love', 'enemy', 'other')),
    contact_number INTEGER, -- For tracking multiple contacts of same type
    name TEXT NOT NULL,
    
    -- Enemy-specific fields
    who_wronged TEXT,
    what_caused TEXT,
    what_throw_down TEXT,
    what_happened TEXT,
    
    notes TEXT,
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Status effects table
CREATE TABLE IF NOT EXISTS status_effects (
    effect_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    effect_name TEXT NOT NULL,
    effect_type TEXT CHECK(effect_type IN ('buff', 'debuff', 'condition', 'other')),
    description TEXT,
    duration TEXT,
    active BOOLEAN DEFAULT 1,
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Critical injuries table
CREATE TABLE IF NOT EXISTS critical_injuries (
    injury_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    injury_name TEXT NOT NULL,
    description TEXT,
    date_received TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    healed BOOLEAN DEFAULT 0,
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Addictions table
CREATE TABLE IF NOT EXISTS addictions (
    addiction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    substance TEXT NOT NULL,
    severity TEXT CHECK(severity IN ('mild', 'moderate', 'severe')),
    notes TEXT,
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Reputation table
CREATE TABLE IF NOT EXISTS reputation (
    reputation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    reputation_score INTEGER DEFAULT 0,
    reputation_event TEXT,
    notes TEXT,
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Stats table
CREATE TABLE IF NOT EXISTS stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    
    -- Core Stats
    intelligence INTEGER DEFAULT 0,
    reflexes INTEGER DEFAULT 0,
    dexterity INTEGER DEFAULT 0,
    technique INTEGER DEFAULT 0,
    cool INTEGER DEFAULT 0,
    willpower INTEGER DEFAULT 0,
    luck INTEGER DEFAULT 0,
    movement INTEGER DEFAULT 0,
    body INTEGER DEFAULT 0,
    empathy INTEGER DEFAULT 0,
    
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Items database
CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    item_type TEXT CHECK(item_type IN ('weapon', 'armor', 'gear', 'cyberware', 'consumable', 'misc')),
    description TEXT,
    value INTEGER DEFAULT 0,
    damage TEXT, -- For weapons
    armor_value INTEGER, -- For armor
    special_properties TEXT,
    is_unique BOOLEAN DEFAULT 0
);

-- Inventory table
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    equipped BOOLEAN DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);

-- Ammo table
CREATE TABLE IF NOT EXISTS ammo (
    ammo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    ammo_type TEXT NOT NULL,
    description TEXT,
    quantity INTEGER DEFAULT 0,
    special_properties TEXT,
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Cybernetics table
CREATE TABLE IF NOT EXISTS cybernetics (
    cybernetic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    cybernetic_name TEXT NOT NULL,
    body_location TEXT,
    description TEXT,
    humanity_cost INTEGER DEFAULT 0,
    installed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    malfunction BOOLEAN DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Maps table (kartat)
CREATE TABLE IF NOT EXISTS maps (
    map_id INTEGER PRIMARY KEY AUTOINCREMENT,
    map_name TEXT NOT NULL,
    description TEXT,
    map_type TEXT CHECK(map_type IN ('district', 'building', 'combat', 'world', 'other')),
    image_path TEXT,
    data TEXT, -- JSON data for map markers, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Character-Map relationship (for tracking which maps are relevant to which characters)
CREATE TABLE IF NOT EXISTS character_maps (
    character_id INTEGER NOT NULL,
    map_id INTEGER NOT NULL,
    notes TEXT,
    PRIMARY KEY (character_id, map_id),
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (map_id) REFERENCES maps(map_id) ON DELETE CASCADE
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_characters_user ON characters(user_id);
CREATE INDEX IF NOT EXISTS idx_inventory_character ON inventory(character_id);
CREATE INDEX IF NOT EXISTS idx_stats_character ON stats(character_id);
CREATE INDEX IF NOT EXISTS idx_contacts_character ON contacts(character_id);
CREATE INDEX IF NOT EXISTS idx_cybernetics_character ON cybernetics(character_id);
