# Cyberpunk Tracker API

Flask REST API for serving character data from SQLite database to the frontend.

## Setup

### 1. Install Dependencies

```bash
cd api
pip3 install -r requirements.txt
```

Or install packages individually:

```bash
pip3 install Flask flask-cors
```

### 2. Make sure the database exists

```bash
cd ../database
python3 init_db.py
python3 example_data.py
```

## Running the API

### Start the server

```bash
cd api
python3 app.py
```

The server will start on `http://localhost:5000`

You should see:
```
Starting Cyberpunk Tracker API...
Database path: /path/to/database/cyberpunk_tracker.db
API will be available at: http://localhost:5000

Endpoints:
  GET  /api/health
  GET  /api/characters
  GET  /api/character/<id>
  PUT  /api/character/<id>
```

### Test the API

Open another terminal and test:

```bash
# Health check
curl http://localhost:5000/api/health

# Get all characters
curl http://localhost:5000/api/characters

# Get specific character
curl http://localhost:5000/api/character/1
```

## API Endpoints

### GET /api/health
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "message": "Cyberpunk Tracker API is running"
}
```

### GET /api/characters
List all characters

**Response:**
```json
[
  {
    "character_id": 1,
    "handle": "V",
    "role": "Solo"
  }
]
```

### GET /api/character/{id}
Get complete character information

**Response:**
```json
{
  "character": {
    "character_id": 1,
    "handle": "V",
    "role": "Solo",
    "role_ability": "Combat Awareness",
    "rank": 4,
    "hp": 35,
    "max_hp": 40,
    "humanity": 43,
    "languages": "English, Streetslang, Japanese",
    ...
  },
  "background": {
    "family_background": "Nomad family...",
    "childhood_environment": "Urban Combat Zone..."
  },
  "contacts": {
    "friends": [...],
    "loves": [...],
    "enemies": [...]
  },
  "critical_injuries": [...],
  "addictions": [...],
  "reputation": {...}
}
```

### PUT /api/character/{id}
Update character information

**Request Body:**
```json
{
  "character": {
    "handle": "V",
    "role": "Solo",
    ...
  },
  "background": {
    "family_background": "...",
    "childhood_environment": "..."
  },
  "contacts": {
    "friends": [
      {"name": "Jackie Welles", "notes": "Best friend"}
    ],
    "loves": [...],
    "enemies": [...]
  },
  "reputation": {
    "reputation_score": 7,
    "reputation_event": "Successful gigs..."
  },
  "critical_injuries": "Cracked ribs\nBroken arm",
  "addictions": "Nicotine\nCoffee"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Character updated successfully"
}
```

## CORS Configuration

The API has CORS enabled to allow requests from the frontend. This is necessary for the web interface to communicate with the API.

## Database Connection

The API uses the `DatabaseHelper` class from `../database/db_helper.py` to interact with the SQLite database at `../database/cyberpunk_tracker.db`.

## Character Selection

Currently, the API and frontend are hardcoded to use `character_id = 1`. In a production environment, you would:

1. Implement user authentication
2. Create a session management system
3. Allow users to select which character to view/edit
4. Pass the character_id from the frontend

## Development Notes

- The API runs in debug mode by default (auto-reloads on code changes)
- All database operations are logged to console
- Errors return JSON with error messages and appropriate HTTP status codes

## Troubleshooting

### Port already in use
If port 5000 is already in use, change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or another port
```

And update `API_BASE_URL` in `js/bio-data-db.js`:
```javascript
const API_BASE_URL = 'http://localhost:5001/api';
```

### Database not found
Make sure you've initialized the database:
```bash
cd ../database
python3 init_db.py
```

### CORS errors
If you see CORS errors in the browser console, make sure flask-cors is installed:
```bash
pip3 install flask-cors
```

### Module not found: db_helper
Make sure the database directory is in the Python path. The `app.py` file adds it automatically, but if you're having issues, you can set it manually:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/../database"
```
