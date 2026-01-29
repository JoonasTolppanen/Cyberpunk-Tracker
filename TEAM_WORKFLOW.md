# Team Workflow - Quick Reference

## How Database Works in This Project

```
┌─────────────────────────────────────────────────────────┐
│                    Git Repository                       │
│  ✅ schema.sql (structure)                              │
│  ✅ init_db.py (create database)                        │
│  ✅ example_data.py (sample data)                       │
│  ❌ *.db files (NOT in git)                             │ 
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┐
        ↓                                    ↓
┌───────────────┐                   ┌───────────────┐
│  Developer 1  │                   │  Developer 2  │
│               │                   │               │
│  git clone    │                   │  git clone    │
│      ↓        │                   │      ↓        │
│  init_db.py   │                   │  init_db.py   │
│      ↓        │                   │      ↓        │
│  local.db     │                   │  local.db     │
│               │                   │               │
└───────────────┘                   └───────────────┘
```

**Key Point**: Each developer has their own local database created from `schema.sql`

---

## Common Scenarios

### New Team Member Joins

```bash
# 1. Clone
git clone <repo-url>

# 2. Create database
cd database
python3 init_db.py
python3 example_data.py

# 3. Install dependencies
cd ../api
pip3 install Flask flask-cors

# 4. Done! Start coding
```

---

### Someone Updates the Schema

**Person making changes:**
```bash
# 1. Edit schema.sql
vim database/schema.sql

# 2. Test locally
cd database
rm cyberpunk_tracker.db
python3 init_db.py
python3 test_db.py

# 3. Commit and push
git add database/schema.sql
git commit -m "Add username field to users table"
git push

# 4. Notify team: "Schema updated - recreate your database!"
```

**Everyone else:**
```bash
# 1. Pull changes
git pull

# 2. Recreate database
cd database
rm cyberpunk_tracker.db
python3 init_db.py
python3 example_data.py

# 3. Continue working
```

---

### Daily Development

```bash
# Morning:
git pull                          # Get latest code
cd api && python3 app.py          # Start API
python3 -m http.server 8080       # Start web server

# Work on features...
# Edit HTML, CSS, JS, Python files

# End of day:
git add .
git commit -m "Add feature X"
git push
```

---

### Testing Changes

```bash
# Test database
cd database
python3 test_db.py

# Test API
curl http://localhost:5000/api/health

# Test website
# Open browser: http://localhost:8080/html/index.html
```

---

## Important Rules

### DO Commit These:
- `schema.sql` - Database structure
- All `.py`, `.js`, `.html`, `.css` files
- `requirements.txt`
- Documentation (`.md` files)
- Scripts (`init_db.py`, etc.)

### DO NOT Commit These:
- `*.db` - Database files
- `__pycache__/` - Python cache
- `venv/` - Virtual environments
- `.vscode/`, `.idea/` - IDE settings
- Personal test data

### When to Recreate Database:

**Recreate after:**
- Git pull that includes `schema.sql` changes
- Switching branches with different schemas
- Database corruption or issues
- Want fresh start with clean data

**Don't need to recreate for:**
- Changes to Python code
- Changes to HTML/CSS/JS
- Changes to API endpoints
- Changes to documentation

---

## Collaboration Tips

### Before Making Schema Changes:

1. **Discuss** with team
2. **Plan** the changes
3. **Test** thoroughly
4. **Document** in commit message
5. **Announce** to team after push

### When You Pull Schema Changes:

1. **Read** the commit message
2. **Understand** what changed
3. **Recreate** your database
4. **Test** that everything works
5. **Ask** if unclear

### If Database Conflicts:

There are no database conflicts! Each person has their own local database. Only the schema (`.sql` file) is in git.

---

## Getting Help

**Database Issues:**
- Check `database/README.md`
- Run `python3 test_db.py`
- Delete and recreate database

**API Issues:**
- Check `api/README.md`
- Test with `curl http://localhost:5000/api/health`
- Check console for errors

**Website Issues:**
- Check browser console (F12)
- Verify both servers running
- Check `SETUP.md`

**Still Stuck:**
- Ask in team chat
- Check existing issues in git
- Read the documentation files

---

## Documentation Index

- **SETUP.md** - Complete setup guide - start here
- **README.md** - Project overview
- **api/README.md** - API documentation
- **database/README.md** - Database documentation
- **database/QUICKSTART.md** - Quick database guide
- **TEAM_WORKFLOW.md** - This file

---

## Remember

1. **Database files are local** - not in git
2. **Schema is shared** - in git as `schema.sql`
3. **Everyone creates their own database** from the schema
4. **Schema changes require database recreation** for all team members
5. **Coordinate schema changes** with the team

---