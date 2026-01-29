#!/usr/bin/env python3
"""
Flask API for Cyberpunk Tracker
Serves character data from SQLite database to frontend
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
import os

# Add database directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from db_helper import DatabaseHelper

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize database helper
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'cyberpunk_tracker.db')
db = DatabaseHelper(db_path)

# For demo, we'll use character_id = 1
# In production, you'd have user authentication and select the appropriate character
DEFAULT_CHARACTER_ID = 1


@app.route('/api/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    """Get complete character information"""
    try:
        # Get character basic info
        character = db.get_character(character_id)
        if not character:
            return jsonify({'error': 'Character not found'}), 404
        
        # Get related data
        background = db.execute_query(
            "SELECT * FROM background WHERE character_id = ?", 
            (character_id,)
        )
        background = background[0] if background else {}
        
        contacts = db.get_character_contacts(character_id)
        
        # Get critical injuries
        injuries = db.execute_query(
            "SELECT * FROM critical_injuries WHERE character_id = ? AND healed = 0",
            (character_id,)
        )
        
        # Get addictions
        addictions = db.execute_query(
            "SELECT * FROM addictions WHERE character_id = ?",
            (character_id,)
        )
        
        # Get reputation
        reputation = db.execute_query(
            "SELECT * FROM reputation WHERE character_id = ?",
            (character_id,)
        )
        
        # Organize contacts by type
        friends = [c for c in contacts if c['contact_type'] == 'friend']
        loves = [c for c in contacts if c['contact_type'] == 'love']
        enemies = [c for c in contacts if c['contact_type'] == 'enemy']
        
        # Build response
        response = {
            'character': character,
            'background': background,
            'contacts': {
                'friends': friends,
                'loves': loves,
                'enemies': enemies
            },
            'critical_injuries': injuries,
            'addictions': addictions,
            'reputation': reputation[0] if reputation else {}
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/character/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    """Update character information"""
    try:
        data = request.json
        
        # Update character basic info
        if 'character' in data:
            char_data = data['character']
            db.update_character(character_id, **char_data)
        
        # Update background
        if 'background' in data:
            bg_data = data['background']
            # Check if background exists
            existing = db.execute_query(
                "SELECT background_id FROM background WHERE character_id = ?",
                (character_id,)
            )
            if existing:
                # Update existing background
                set_clause = ', '.join([f"{key} = ?" for key in bg_data.keys()])
                values = list(bg_data.values()) + [character_id]
                db.execute_update(
                    f"UPDATE background SET {set_clause} WHERE character_id = ?",
                    tuple(values)
                )
            else:
                # Create new background
                fields = ['character_id'] + list(bg_data.keys())
                values = [character_id] + list(bg_data.values())
                placeholders = ', '.join(['?'] * len(values))
                db.execute_update(
                    f"INSERT INTO background ({', '.join(fields)}) VALUES ({placeholders})",
                    tuple(values)
                )
        
        # Update contacts (delete and recreate for simplicity)
        if 'contacts' in data:
            # Delete existing contacts
            db.execute_update("DELETE FROM contacts WHERE character_id = ?", (character_id,))
            
            # Add new contacts
            contacts_data = data['contacts']
            
            # Add friends
            for i, friend in enumerate(contacts_data.get('friends', []), 1):
                if friend.get('name'):
                    db.add_contact(
                        character_id, 
                        'friend', 
                        friend['name'],
                        contact_number=i,
                        notes=friend.get('notes', '')
                    )
            
            # Add loves
            for i, love in enumerate(contacts_data.get('loves', []), 1):
                if love.get('name'):
                    db.add_contact(
                        character_id,
                        'love',
                        love['name'],
                        contact_number=i,
                        notes=love.get('notes', '')
                    )
            
            # Add enemies
            for i, enemy in enumerate(contacts_data.get('enemies', []), 1):
                if enemy.get('name'):
                    db.add_contact(
                        character_id,
                        'enemy',
                        enemy['name'],
                        contact_number=i,
                        who_wronged=enemy.get('who_wronged', ''),
                        what_caused=enemy.get('what_caused', ''),
                        what_throw_down=enemy.get('what_throw_down', ''),
                        what_happened=enemy.get('what_happened', ''),
                        notes=enemy.get('notes', '')
                    )
        
        # Update reputation
        if 'reputation' in data:
            rep_data = data['reputation']
            existing = db.execute_query(
                "SELECT reputation_id FROM reputation WHERE character_id = ?",
                (character_id,)
            )
            if existing:
                set_clause = ', '.join([f"{key} = ?" for key in rep_data.keys()])
                values = list(rep_data.values()) + [character_id]
                db.execute_update(
                    f"UPDATE reputation SET {set_clause} WHERE character_id = ?",
                    tuple(values)
                )
            else:
                fields = ['character_id'] + list(rep_data.keys())
                values = [character_id] + list(rep_data.values())
                placeholders = ', '.join(['?'] * len(values))
                db.execute_update(
                    f"INSERT INTO reputation ({', '.join(fields)}) VALUES ({placeholders})",
                    tuple(values)
                )
        
        # Update critical injuries (delete and recreate)
        if 'critical_injuries' in data:
            db.execute_update(
                "DELETE FROM critical_injuries WHERE character_id = ? AND healed = 0",
                (character_id,)
            )
            injuries_text = data['critical_injuries']
            if injuries_text:
                # Split by lines and create separate entries
                for injury_line in injuries_text.split('\n'):
                    if injury_line.strip():
                        db.execute_update(
                            "INSERT INTO critical_injuries (character_id, injury_name, description) VALUES (?, ?, ?)",
                            (character_id, injury_line[:50], injury_line)
                        )
        
        # Update addictions (delete and recreate)
        if 'addictions' in data:
            db.execute_update(
                "DELETE FROM addictions WHERE character_id = ?",
                (character_id,)
            )
            addictions_text = data['addictions']
            if addictions_text:
                # Split by lines and create separate entries
                for addiction_line in addictions_text.split('\n'):
                    if addiction_line.strip():
                        db.execute_update(
                            "INSERT INTO addictions (character_id, substance, severity) VALUES (?, ?, ?)",
                            (character_id, addiction_line[:50], 'mild')
                        )
        
        return jsonify({'success': True, 'message': 'Character updated successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/characters', methods=['GET'])
def list_characters():
    """List all characters (for future character selection)"""
    try:
        characters = db.execute_query("SELECT character_id, handle, role FROM characters ORDER BY handle")
        return jsonify(characters)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({'status': 'ok', 'message': 'Cyberpunk Tracker API is running'})


if __name__ == '__main__':
    print("Starting Cyberpunk Tracker API...")
    print(f"Database path: {db_path}")
    print("API will be available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /api/health")
    print("  GET  /api/characters")
    print("  GET  /api/character/<id>")
    print("  PUT  /api/character/<id>")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
