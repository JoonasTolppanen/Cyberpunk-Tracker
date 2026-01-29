# Team Setup Guide

Quick guide for team members to get the project running on their machine.

---

## 🚀 First Time Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Softa_2
```

### 2. Set Up the Database

The database file (`*.db`) is **NOT** in git (it's in `.gitignore`). Each team member creates their own local database:

```bash
cd database
python3 init_db.py
```

This creates `cyberpunk_tracker.db` with all tables defined in `schema.sql`.

### 3. Add Example Data (Optional)

Load sample characters and data for testing:

```bash
python3 example_data.py
```

This creates:
- 2 users (demo_player, gm)
- 2 characters (V, Johnny Silverhand)
- Sample items, contacts, cybernetics, etc.

### 4. Install API Dependencies

```bash
cd ../api
pip3 install -r requirements.txt
```

Or manually:
```bash
pip3 install Flask flask-cors
```

### 5. Start the Servers

**Terminal 1 - API Server:**
```bash
cd api
python3 app.py
```

**Terminal 2 - Web Server:**
```bash
cd Softa_2  # project root
python3 -m http.server 8080
```

### 6. Open the Website

Navigate to: `http://localhost:8080/html/index.html`

---

## 📋 Quick Start (One Command)

```bash
cd api
./start_server.sh
```

Then open `http://localhost:8080/html/index.html`

---

## 🔄 Daily Workflow

### Starting Work

```bash
# Terminal 1
cd api && python3 app.py

# Terminal 2  
python3 -m http.server 8080

# Open browser: http://localhost:8080/html/index.html
```

### Pull Latest Changes

```bash
git pull
```

**If schema changed** (you'll see updates to `schema.sql`):

```bash
cd database
rm cyberpunk_tracker.db  # Delete old database
python3 init_db.py       # Recreate with new schema
python3 example_data.py  # Reload sample data
```

---

## 📂 What's in Git vs Not

### ✅ In Git (Shared)

- **Schema**: `database/schema.sql` - Database structure
- **Code**: All `.py`, `.js`, `.html`, `.css` files
- **Scripts**: `init_db.py`, `example_data.py`, `db_helper.py`
- **Docs**: README files and documentation

### ❌ NOT in Git (Local Only)

- **Database files**: `*.db`, `*.sqlite`
- **Python cache**: `__pycache__/`, `*.pyc`
- **Virtual environments**: `venv/`, `env/`
- **IDE settings**: `.vscode/`, `.idea/`
- **Logs**: `*.log`

---

## 🛠️ Making Database Changes

### If You Need to Change the Schema:

1. **Edit** `database/schema.sql`
2. **Test locally**:
   ```bash
   cd database
   rm cyberpunk_tracker.db
   python3 init_db.py
   python3 test_db.py  # Verify it works
   ```
3. **Commit** the schema changes:
   ```bash
   git add database/schema.sql
   git commit -m "Update schema: [describe change]"
   git push
   ```
4. **Notify team** that they need to recreate their database

### Team Member Updates Their Database:

```bash
git pull
cd database
rm cyberpunk_tracker.db
python3 init_db.py
python3 example_data.py  # If you want sample data
```

---

## 🧪 Testing Your Setup

### 1. Test Database Connection

```bash
cd database
python3 test_db.py
```

Expected: "✓ All tests passed!"

### 2. Test API

```bash
curl http://localhost:5000/api/health
```

Expected: `{"status":"ok"}`

### 3. Test Website

Open browser to `http://localhost:8080/html/index.html`

Expected: See character bio page with data loaded

---

## 🐛 Troubleshooting

### "Database not found"

**Cause**: You haven't created the database yet

**Fix**:
```bash
cd database
python3 init_db.py
```

### "Flask not found" or "Module not found"

**Cause**: Dependencies not installed

**Fix**:
```bash
pip3 install Flask flask-cors
```

### "Address already in use" (port 5000 or 8080)

**Cause**: Server already running or port in use

**Fix**:
```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9  # For API
lsof -ti:8080 | xargs kill -9  # For web server
```

### "No data showing on website"

**Cause**: No data in database

**Fix**:
```bash
cd database
python3 example_data.py
```

### API returns 404 or errors

**Cause**: API server not running

**Fix**: Start API server in another terminal:
```bash
cd api
python3 app.py
```

---

## 👥 Team Coordination

### When Working on Database Schema:

1. **Coordinate** with team before making schema changes
2. **Document** changes in `database/CHANGES.md`
3. **Test** thoroughly before committing
4. **Announce** in team chat when pushing schema changes
5. **Help** teammates update their local databases

### When Adding New Features:

1. **Frontend** (HTML/CSS/JS) - commit directly
2. **Backend** (Python API) - commit directly
3. **Database schema** - coordinate with team
4. **Documentation** - update relevant README files

---

## 📁 Project Structure Reference

```
Softa_2/
├── README.md              # Main project docs
├── SETUP.md              # This file
├── .gitignore            # What NOT to commit
│
├── api/                  # Flask API
│   ├── app.py           # API server
│   ├── requirements.txt # Python dependencies
│   └── README.md        # API documentation
│
├── database/            # Database files
│   ├── schema.sql      # ✅ IN GIT - Database structure
│   ├── init_db.py      # ✅ IN GIT - Create database
│   ├── db_helper.py    # ✅ IN GIT - Database utilities
│   ├── example_data.py # ✅ IN GIT - Sample data
│   ├── test_db.py      # ✅ IN GIT - Tests
│   └── *.db            # ❌ NOT IN GIT - Your local database
│
├── html/               # Web pages
│   └── *.html
├── css/                # Stylesheets
│   └── styles.css
├── js/                 # JavaScript
│   └── *.js
└── images/             # Images
    └── *.png
```

---

## 🎯 Summary

**For new team members:**
1. Clone repo
2. Run `python3 database/init_db.py`
3. Run `python3 database/example_data.py`
4. Install Flask: `pip3 install Flask flask-cors`
5. Start API: `cd api && python3 app.py`
6. Start web: `python3 -m http.server 8080`
7. Open browser: `http://localhost:8080/html/index.html`

**After git pull (if schema changed):**
1. Delete database: `rm database/cyberpunk_tracker.db`
2. Recreate: `python3 database/init_db.py`
3. Reload data: `python3 database/example_data.py`

**The database is local** - each team member has their own copy for development!

---

Need help? Check the documentation:
- Main: `README.md`
- Database: `database/README.md`
- API: `api/README.md`
- Quick Start: `database/QUICKSTART.md`
