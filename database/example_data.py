#!/usr/bin/env python3
"""
Example data script for Cyberpunk Tracker
Populates the database with sample characters and data for testing
"""

from db_helper import DatabaseHelper
import hashlib

def hash_password(password: str) -> str:
    """Simple password hashing (use proper hashing in production!)"""
    return hashlib.sha256(password.encode()).hexdigest()

def populate_example_data(db_path='cyberpunk_tracker.db'):
    """Populate database with example data"""
    
    db = DatabaseHelper(db_path)
    
    print("Populating database with example data...")
    print("=" * 50)
    
    # Create example users
    print("\n1. Creating users...")
    user1_id = db.create_user('demo_player', hash_password('demo123'))
    user2_id = db.create_user('gm', hash_password('gm123'))
    print(f"  ✓ Created user 'demo_player' (ID: {user1_id})")
    print(f"  ✓ Created user 'gm' (ID: {user2_id})")
    
    # Create example character: V (Solo)
    print("\n2. Creating character 'V' (Solo)...")
    v_id = db.create_character(
        user_id=user1_id,
        handle='V',
        role='Solo',
        role_ability='Combat Awareness',
        rank=4,
        ability='Can perceive threats and attack 3 enemies in one turn',
        hp=35,
        max_hp=40,
        humanity=43,
        max_humanity=50,
        death_save=3,
        cultural_region='North America - Street',
        clothing_style='Edgerunner Casual',
        hairstyle='Undercut with neon highlights',
        affectation='Always checks exits in a room',
        languages='English, Streetslang, Japanese',
        improvement_points=12,
        notes='Veteran Solo, specializes in close combat'
    )
    print(f"  ✓ Created character 'V' (ID: {v_id})")
    
    # Add V's stats
    print("\n3. Setting character stats...")
    db.set_character_stats(
        v_id,
        intelligence=6,
        reflexes=8,
        dexterity=7,
        technique=5,
        cool=7,
        willpower=6,
        luck=4,
        movement=6,
        body=7,
        empathy=4
    )
    print("  ✓ Stats set for V")
    
    # Add V's background
    print("\n4. Adding background information...")
    db.execute_update(
        "INSERT INTO background (character_id, family_background, childhood_environment) VALUES (?, ?, ?)",
        (v_id, 'Nomad family, lost contact after corp raid', 'Urban Combat Zone - learned to fight early')
    )
    print("  ✓ Background added")
    
    # Add contacts
    print("\n5. Adding contacts...")
    db.add_contact(v_id, 'friend', 'Jackie Welles', contact_number=1, 
                   notes='Best friend and partner, loyal to the end')
    db.add_contact(v_id, 'friend', 'Misty Olszewski', contact_number=2,
                   notes='Spiritual guide and friend')
    db.add_contact(v_id, 'love', 'Judy Alvarez', contact_number=1,
                   notes='Braindance technician, complicated relationship')
    db.add_contact(v_id, 'enemy', 'Arasaka Corporation', contact_number=1,
                   who_wronged='They wronged me',
                   what_caused='Betrayed during a heist',
                   what_throw_down='Public humiliation',
                   what_happened='Still hunting me')
    print("  ✓ Added 2 friends, 1 love interest, 1 enemy")
    
    # Add cybernetics
    print("\n6. Installing cybernetics...")
    db.add_cybernetic(v_id, 'Mantis Blades', 'Arms', humanity_cost=7,
                     description='Retractable blade implants for close combat')
    db.add_cybernetic(v_id, 'Kerenzikov', 'Nervous System', humanity_cost=5,
                     description='Boosts reflexes when dodging, allows quick response')
    db.add_cybernetic(v_id, 'Optical Camo', 'Integumentary System', humanity_cost=7,
                     description='Makes user nearly invisible for short periods')
    print("  ✓ Installed 3 cybernetic implants")
    
    # Add critical injuries and addictions
    print("\n7. Adding status conditions...")
    db.execute_update(
        "INSERT INTO critical_injuries (character_id, injury_name, description) VALUES (?, ?, ?)",
        (v_id, 'Cracked Ribs', 'Took heavy damage in last firefight, -2 to BODY checks')
    )
    db.execute_update(
        "INSERT INTO addictions (character_id, substance, severity, notes) VALUES (?, ?, ?, ?)",
        (v_id, 'Nicotine', 'mild', 'Chain smoker, helps with stress')
    )
    print("  ✓ Added 1 critical injury and 1 addiction")
    
    # Add reputation
    print("\n8. Setting reputation...")
    db.execute_update(
        "INSERT INTO reputation (character_id, reputation_score, reputation_event) VALUES (?, ?, ?)",
        (v_id, 7, 'Successful gigs in Watson, saved Aldecaldos member')
    )
    print("  ✓ Reputation set")
    
    # Create some items
    print("\n9. Creating items...")
    items_data = [
        ('Militech M-10AF Lexington', 'weapon', 'Medium Pistol, 2d6 damage', 500, '2d6', None, 'Standard sidearm'),
        ('Arasaka HJKE-11 Yukimura', 'weapon', 'Heavy Pistol, 3d6 damage', 1000, '3d6', None, 'High-powered pistol'),
        ('Kevlar Vest', 'armor', 'Body armor', 500, None, 11, 'Stops small arms fire'),
        ('Medkit', 'consumable', 'First aid supplies', 50, None, None, 'Heals 2d6 HP'),
        ('Braindance Wreath', 'gear', 'BD playback device', 100, None, None, 'For experiencing BDs'),
    ]
    
    item_ids = []
    for item_data in items_data:
        query = "INSERT INTO items (item_name, item_type, description, value, damage, armor_value, special_properties) VALUES (?, ?, ?, ?, ?, ?, ?)"
        item_id = db.execute_update(query, item_data)
        item_ids.append(item_id)
    print(f"  ✓ Created {len(items_data)} items")
    
    # Add items to V's inventory
    print("\n10. Adding items to inventory...")
    db.add_item_to_inventory(v_id, item_ids[0], 1)  # Lexington pistol
    db.add_item_to_inventory(v_id, item_ids[2], 1)  # Kevlar vest
    db.add_item_to_inventory(v_id, item_ids[3], 3)  # 3 medkits
    db.add_item_to_inventory(v_id, item_ids[4], 1)  # BD wreath
    
    # Mark some as equipped
    db.execute_update("UPDATE inventory SET equipped = 1 WHERE character_id = ? AND item_id = ?", (v_id, item_ids[0]))
    db.execute_update("UPDATE inventory SET equipped = 1 WHERE character_id = ? AND item_id = ?", (v_id, item_ids[2]))
    print("  ✓ Added items to inventory")
    
    # Add ammo
    print("\n11. Adding ammunition...")
    db.execute_update(
        "INSERT INTO ammo (character_id, ammo_type, description, quantity) VALUES (?, ?, ?, ?)",
        (v_id, 'Standard 9mm', 'Standard rounds', 45)
    )
    db.execute_update(
        "INSERT INTO ammo (character_id, ammo_type, description, quantity, special_properties) VALUES (?, ?, ?, ?, ?)",
        (v_id, 'Armor-Piercing 9mm', '9mm armor-piercing rounds', 12, 'Ignores 4 points of armor')
    )
    print("  ✓ Added ammo types")
    
    # Create a map
    print("\n12. Creating map...")
    map_id = db.execute_update(
        "INSERT INTO maps (map_name, description, map_type, data) VALUES (?, ?, ?, ?)",
        ('Watson - Little China', 'Dense urban district with heavy Asian influence', 'district',
         '{"markers": [{"x": 100, "y": 150, "label": "Vs Apartment"}, {"x": 200, "y": 180, "label": "Mistys Shop"}]}')
    )
    
    # Link map to character
    db.execute_update(
        "INSERT INTO character_maps (character_id, map_id, notes) VALUES (?, ?, ?)",
        (v_id, map_id, 'Home territory')
    )
    print(f"  ✓ Created map and linked to character")
    
    # Create second character: Johnny Silverhand (Rockerboy)
    print("\n13. Creating character 'Johnny Silverhand' (Rockerboy)...")
    johnny_id = db.create_character(
        user_id=user2_id,
        handle='Johnny Silverhand',
        role='Rockerboy',
        role_ability='Charismatic Impact',
        rank=8,
        hp=30,
        max_hp=40,
        humanity=20,
        max_humanity=50,
        cultural_region='North America',
        clothing_style='Punk Rock Icon',
        hairstyle='Long dark hair',
        affectation='Always wears aviator sunglasses',
        languages='English, Streetslang',
        notes='Legendary rockerboy and rebel'
    )
    
    db.set_character_stats(
        johnny_id,
        intelligence=7,
        reflexes=7,
        dexterity=6,
        technique=8,
        cool=9,
        willpower=8,
        luck=3,
        movement=5,
        body=6,
        empathy=3
    )
    print(f"  ✓ Created character 'Johnny Silverhand' (ID: {johnny_id})")
    
    print("\n" + "=" * 50)
    print("✓ Example data population complete!")
    print("\nSummary:")
    print(f"  - {db.get_table_count('users')} users")
    print(f"  - {db.get_table_count('characters')} characters")
    print(f"  - {db.get_table_count('items')} items")
    print(f"  - {db.get_table_count('inventory')} inventory entries")
    print(f"  - {db.get_table_count('contacts')} contacts")
    print(f"  - {db.get_table_count('cybernetics')} cybernetics")
    print(f"  - {db.get_table_count('maps')} maps")
    
    return v_id, johnny_id

if __name__ == '__main__':
    import sys
    
    db_path = 'cyberpunk_tracker.db'
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    try:
        populate_example_data(db_path)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the database has been initialized first:")
        print("  python3 init_db.py")
        sys.exit(1)
