#!/usr/bin/env python3
"""
Quick test script to verify database functionality
"""

from db_helper import DatabaseHelper
import os

def test_database():
    """Run basic tests on database functionality"""
    
    # Use a test database
    test_db_path = 'test_cyberpunk.db'
    
    # Remove if exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    print("Running database tests...")
    print("=" * 50)
    
    # Initialize database
    print("\n1. Initializing test database...")
    from init_db import init_database
    if not init_database(test_db_path):
        print("❌ Failed to initialize database")
        return False
    
    db = DatabaseHelper(test_db_path)
    
    # Test 1: Create user
    print("\n2. Testing user creation...")
    try:
        user_id = db.create_user('test_user', 'hashed_password')
        user = db.get_user(user_id)
        assert user['username'] == 'test_user'
        print(f"  ✓ User created (ID: {user_id})")
    except Exception as e:
        print(f"  ❌ User creation failed: {e}")
        return False
    
    # Test 2: Create character
    print("\n3. Testing character creation...")
    try:
        char_id = db.create_character(user_id, 'TestChar', role='Solo', hp=40)
        char = db.get_character(char_id)
        assert char['handle'] == 'TestChar'
        assert char['hp'] == 40
        print(f"  ✓ Character created (ID: {char_id})")
    except Exception as e:
        print(f"  ❌ Character creation failed: {e}")
        return False
    
    # Test 3: Set stats
    print("\n4. Testing stats management...")
    try:
        db.set_character_stats(char_id, intelligence=7, reflexes=8, cool=6)
        stats = db.get_character_stats(char_id)
        assert stats['intelligence'] == 7
        assert stats['reflexes'] == 8
        print("  ✓ Stats set successfully")
    except Exception as e:
        print(f"  ❌ Stats management failed: {e}")
        return False
    
    # Test 4: Add contact
    print("\n5. Testing contact management...")
    try:
        contact_id = db.add_contact(char_id, 'friend', 'Test Friend', contact_number=1)
        contacts = db.get_character_contacts(char_id, 'friend')
        assert len(contacts) == 1
        assert contacts[0]['name'] == 'Test Friend'
        print("  ✓ Contact added successfully")
    except Exception as e:
        print(f"  ❌ Contact management failed: {e}")
        return False
    
    # Test 5: Add cybernetic
    print("\n6. Testing cybernetics management...")
    try:
        cyber_id = db.add_cybernetic(char_id, 'Test Implant', 'Arm', humanity_cost=5)
        cybernetics = db.get_character_cybernetics(char_id)
        assert len(cybernetics) == 1
        assert cybernetics[0]['cybernetic_name'] == 'Test Implant'
        print("  ✓ Cybernetic added successfully")
    except Exception as e:
        print(f"  ❌ Cybernetics management failed: {e}")
        return False
    
    # Test 6: Inventory management
    print("\n7. Testing inventory management...")
    try:
        # Create an item
        item_id = db.execute_update(
            "INSERT INTO items (item_name, item_type, value) VALUES (?, ?, ?)",
            ('Test Pistol', 'weapon', 500)
        )
        
        # Add to inventory
        db.add_item_to_inventory(char_id, item_id, quantity=2)
        inventory = db.get_character_inventory(char_id)
        assert len(inventory) == 1
        assert inventory[0]['quantity'] == 2
        print("  ✓ Inventory management working")
    except Exception as e:
        print(f"  ❌ Inventory management failed: {e}")
        return False
    
    # Test 7: Update character
    print("\n8. Testing character updates...")
    try:
        db.update_character(char_id, hp=35, notes='Test update')
        updated_char = db.get_character(char_id)
        assert updated_char['hp'] == 35
        assert updated_char['notes'] == 'Test update'
        print("  ✓ Character updated successfully")
    except Exception as e:
        print(f"  ❌ Character update failed: {e}")
        return False
    
    # Clean up
    print("\n9. Cleaning up...")
    os.remove(test_db_path)
    print("  ✓ Test database removed")
    
    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    return True

if __name__ == '__main__':
    import sys
    
    try:
        success = test_database()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
