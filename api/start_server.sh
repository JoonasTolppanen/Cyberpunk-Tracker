#!/bin/bash
# Start the Cyberpunk Tracker API server

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Cyberpunk Tracker API Server ===${NC}"
echo ""

# Check if database exists
DB_PATH="../database/cyberpunk_tracker.db"
if [ ! -f "$DB_PATH" ]; then
    echo -e "${YELLOW}⚠ Database not found at $DB_PATH${NC}"
    echo -e "${YELLOW}Creating database...${NC}"
    cd ../database
    python3 init_db.py
    python3 example_data.py
    cd ../api
    echo -e "${GREEN}✓ Database created${NC}"
    echo ""
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠ Flask not installed${NC}"
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip3 install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
    echo ""
fi

# Start the server
echo -e "${GREEN}Starting API server...${NC}"
echo ""
echo -e "Server will be available at: ${GREEN}http://localhost:5000${NC}"
echo -e "Open your browser and navigate to: ${GREEN}../html/index.html${NC}"
echo ""
echo -e "Press ${YELLOW}Ctrl+C${NC} to stop the server"
echo ""

python3 app.py
