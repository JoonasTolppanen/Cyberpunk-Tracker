# Cyberpunk-Tracker
Ohjelmistotuotanto 2 projekti

A web-based character tracker for Cyberpunk RED TTRPG.

## Quick Start for Team Members

**New to the project?** See **[SETUP.md](SETUP.md)** for complete setup instructions.

## Features

- Character biography and background management
- Stats and skills tracking
- Inventory system
- Combat management
- Contact and relationship tracking
- Cybernetics and humanity tracking
- SQLite database backend

## Project Structure

```
Cyberpunk-Tracker/
├── html/              # HTML pages
│   ├── index.html     # Main entry point
│   ├── bio.html       # Character biography display
│   ├── bio-edit.html  # Biography editor
│   ├── stats.html     # Character stats
│   ├── inventory.html # Inventory management
│   └── combat.html    # Combat tracker
├── css/               # Stylesheets
│   └── styles.css
├── js/                # JavaScript files
│   ├── navigation.js     # Page navigation
│   ├── bio-data.js       # Data management - localStorage - legacy
│   └── bio-data-db.js    # Data management - database-backed
├── api/               # Flask REST API
│   ├── app.py            # API server
│   ├── requirements.txt  # Python dependencies
│   ├── start_server.sh   # Quick start script
│   └── README.md         # API documentation
├── database/          # Database files
│   ├── schema.sql        # Database schema
│   ├── init_db.py        # Database initialization
│   ├── db_helper.py      # Database helper functions
│   ├── example_data.py   # Sample data generator
│   └── README.md         # Database documentation
└── images/            # Image assets

```

## Getting Started

### Quick Start (Database-Backed Version)

The easiest way to get started:

```bash
# 1. Start the API server (auto-creates database if needed)
cd api
./start_server.sh

# 2. In another terminal or open in browser
# Open html/index.html in your web browser
```

The API server will:
- ✓ Check if database exists (create it if not)
- ✓ Install Flask dependencies if needed
- ✓ Start the API on http://localhost:5000
- ✓ Enable the web interface to load/save data

### Manual Setup

#### 1. Set Up the Database

```bash
cd database
python3 init_db.py           # Create database
python3 example_data.py      # Add sample data (optional)
```

#### 2. Install API Dependencies

```bash
cd api
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install Flask flask-cors
```

#### 3. Start the API Server

```bash
cd api
python3 app.py
```

The server will start on http://localhost:5000

#### 4. Open the Web Interface

Open `html/index.html` in a web browser. The bio pages will now load and save data from/to the database!

## Database

The project uses SQLite for data persistence with the following tables:

- **users** - User accounts
- **characters** - Character profiles (hahmot)
- **background** - Character backgrounds
- **contacts** - Relationships (contactit)
- **status_effects** - Active status effects
- **critical_injuries** - Injury tracking
- **addictions** - Substance dependencies
- **reputation** - Reputation with factions
- **stats** - Character statistics
- **items** - Item database
- **inventory** - Character inventory
- **ammo** - Ammunition tracking
- **cybernetics** - Cybernetic implants
- **maps** - Game maps (kartat)
- **character_maps** - Character-map relationships

See `database/README.md` for detailed documentation.

## Usage

### Python Database API

```python
from database.db_helper import DatabaseHelper

# Initialize
db = DatabaseHelper('cyberpunk_tracker.db')

# Create a character
char_id = db.create_character(
    user_id=1,
    handle='V',
    role='Solo',
    hp=40,
    max_hp=40
)

# Set stats
db.set_character_stats(char_id, intelligence=7, reflexes=8)

# Add to inventory
db.add_item_to_inventory(char_id, item_id=1, quantity=1)
```

## Development

This project is part of Ohjelmistotuotanto 2 (Software Engineering 2) course.

## How It Works

### Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Web Browser   │ ───────>│   Flask API     │ ───────>│     SQLite      │
│   (HTML/CSS/JS) │  HTTP   │   (Python)      │         │    Database     │
│                 │ <───────│   Port 5000     │ <───────│                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

1. **Frontend (bio.html, bio-edit.html)**: Display and edit character data
2. **JavaScript (bio-data-db.js)**: Fetch/save data via API
3. **Flask API (app.py)**: REST endpoints for CRUD operations
4. **Database Helper (db_helper.py)**: Python interface to SQLite
5. **SQLite Database**: Persistent data storage

### Data Flow

**Loading Character Bio:**
1. Page loads → JavaScript calls `loadBioDataToDisplay()`
2. Fetch GET request to `/api/character/1`
3. API queries database using `db_helper.py`
4. JSON data returned to frontend
5. JavaScript populates HTML elements

**Saving Character Bio:**
1. User clicks "Done Editing" → JavaScript calls `saveBioData()`
2. Collect form data into JSON payload
3. Send PUT request to `/api/character/1`
4. API updates database tables
5. Redirect to display page

## Features

- ✅ Character biography and background management
- ✅ Contact tracking (friends, lovers, enemies)
- ✅ Critical injuries and addictions
- ✅ Reputation and improvement points
- ✅ Identifying features (cultural region, style, etc.)
- ✅ Real-time database synchronization
- ✅ RESTful API backend
- 🚧 Stats and skills tracking (coming soon)
- 🚧 Inventory system (coming soon)
- 🚧 Combat management (coming soon)