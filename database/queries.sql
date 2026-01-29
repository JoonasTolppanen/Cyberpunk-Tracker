-- Common SQL Queries for Cyberpunk Tracker
-- Reference guide for frequently used database operations

-- ============================================
-- USER QUERIES
-- ============================================

-- Get user by username
SELECT * FROM users WHERE username = 'player1';

-- List all users with their character counts
SELECT u.user_id, u.username, COUNT(c.character_id) as character_count
FROM users u
LEFT JOIN characters c ON u.user_id = c.user_id
GROUP BY u.user_id;

-- ============================================
-- CHARACTER QUERIES
-- ============================================

-- Get complete character information
SELECT * FROM characters WHERE character_id = 1;

-- Get all characters for a user
SELECT * FROM characters WHERE user_id = 1 ORDER BY created_date DESC;

-- Get character with stats
SELECT c.*, s.*
FROM characters c
LEFT JOIN stats s ON c.character_id = s.character_id
WHERE c.character_id = 1;

-- Get character summary (name, role, hp, humanity)
SELECT handle, role, hp, max_hp, humanity, max_humanity
FROM characters
WHERE character_id = 1;

-- Search characters by name or role
SELECT * FROM characters 
WHERE handle LIKE '%V%' OR role LIKE '%Solo%';

-- ============================================
-- STATS QUERIES
-- ============================================

-- Get character stats
SELECT * FROM stats WHERE character_id = 1;

-- Calculate total stat points for a character
SELECT 
    character_id,
    (intelligence + reflexes + dexterity + technique + cool + 
     willpower + luck + movement + body + empathy) as total_stats
FROM stats
WHERE character_id = 1;

-- Characters sorted by specific stat (e.g., highest cool)
SELECT c.handle, c.role, s.cool
FROM characters c
JOIN stats s ON c.character_id = s.character_id
ORDER BY s.cool DESC;

-- ============================================
-- INVENTORY QUERIES
-- ============================================

-- Get character's complete inventory with item details
SELECT i.item_name, i.item_type, i.description, inv.quantity, inv.equipped
FROM inventory inv
JOIN items i ON inv.item_id = i.item_id
WHERE inv.character_id = 1
ORDER BY i.item_type, i.item_name;

-- Get only equipped items
SELECT i.item_name, i.item_type, i.damage, i.armor_value
FROM inventory inv
JOIN items i ON inv.item_id = i.item_id
WHERE inv.character_id = 1 AND inv.equipped = 1;

-- Get weapons in inventory
SELECT i.item_name, i.damage, i.special_properties, inv.quantity
FROM inventory inv
JOIN items i ON inv.item_id = i.item_id
WHERE inv.character_id = 1 AND i.item_type = 'weapon';

-- Calculate total inventory value for a character
SELECT SUM(i.value * inv.quantity) as total_value
FROM inventory inv
JOIN items i ON inv.item_id = i.item_id
WHERE inv.character_id = 1;

-- ============================================
-- CONTACTS QUERIES
-- ============================================

-- Get all contacts for a character
SELECT * FROM contacts 
WHERE character_id = 1 
ORDER BY contact_type, contact_number;

-- Get friends only
SELECT name, notes FROM contacts
WHERE character_id = 1 AND contact_type = 'friend'
ORDER BY contact_number;

-- Get enemies with details
SELECT name, who_wronged, what_caused, what_happened
FROM contacts
WHERE character_id = 1 AND contact_type = 'enemy';

-- Count contacts by type
SELECT contact_type, COUNT(*) as count
FROM contacts
WHERE character_id = 1
GROUP BY contact_type;

-- ============================================
-- CYBERNETICS QUERIES
-- ============================================

-- Get all cybernetics for a character
SELECT * FROM cybernetics 
WHERE character_id = 1 
ORDER BY installed_date;

-- Calculate total humanity cost of cybernetics
SELECT SUM(humanity_cost) as total_humanity_loss
FROM cybernetics
WHERE character_id = 1;

-- Get cybernetics by body location
SELECT body_location, GROUP_CONCAT(cybernetic_name, ', ') as implants
FROM cybernetics
WHERE character_id = 1
GROUP BY body_location;

-- Check for malfunctioning cybernetics
SELECT * FROM cybernetics
WHERE character_id = 1 AND malfunction = 1;

-- ============================================
-- STATUS QUERIES
-- ============================================

-- Get active status effects
SELECT * FROM status_effects
WHERE character_id = 1 AND active = 1;

-- Get all critical injuries (not healed)
SELECT * FROM critical_injuries
WHERE character_id = 1 AND healed = 0;

-- Get all addictions
SELECT substance, severity, notes
FROM addictions
WHERE character_id = 1;

-- ============================================
-- REPUTATION QUERIES
-- ============================================

-- Get character reputation
SELECT reputation_event, reputation_score
FROM reputation
WHERE character_id = 1;

-- Characters with highest reputation
SELECT c.handle, r.reputation_event, r.reputation_score
FROM characters c
JOIN reputation r ON c.character_id = r.character_id
ORDER BY r.reputation_score DESC
LIMIT 10;

-- ============================================
-- AMMO QUERIES
-- ============================================

-- Get all ammo for a character
SELECT ammo_type, description, quantity, special_properties
FROM ammo
WHERE character_id = 1
ORDER BY ammo_type;

-- Check low ammo (less than 20 rounds)
SELECT * FROM ammo
WHERE character_id = 1 AND quantity < 20;

-- ============================================
-- MAP QUERIES
-- ============================================

-- Get all maps
SELECT * FROM maps ORDER BY map_type, map_name;

-- Get maps relevant to a character
SELECT m.*
FROM maps m
JOIN character_maps cm ON m.map_id = cm.map_id
WHERE cm.character_id = 1;

-- ============================================
-- COMPLEX QUERIES
-- ============================================

-- Complete character sheet
SELECT 
    c.*,
    s.intelligence, s.reflexes, s.dexterity, s.technique, s.cool,
    s.willpower, s.luck, s.movement, s.body, s.empathy,
    b.family_background, b.childhood_environment
FROM characters c
LEFT JOIN stats s ON c.character_id = s.character_id
LEFT JOIN background b ON c.character_id = b.character_id
WHERE c.character_id = 1;

-- Character wealth and inventory summary
SELECT 
    c.handle,
    COUNT(DISTINCT inv.item_id) as unique_items,
    SUM(inv.quantity) as total_items,
    SUM(i.value * inv.quantity) as total_value
FROM characters c
LEFT JOIN inventory inv ON c.character_id = inv.character_id
LEFT JOIN items i ON inv.item_id = i.item_id
WHERE c.character_id = 1
GROUP BY c.character_id;

-- Character danger level (enemies and critical injuries)
SELECT 
    c.handle,
    COUNT(DISTINCT cont.contact_id) as enemy_count,
    COUNT(DISTINCT ci.injury_id) as injury_count,
    c.hp,
    c.humanity
FROM characters c
LEFT JOIN contacts cont ON c.character_id = cont.character_id AND cont.contact_type = 'enemy'
LEFT JOIN critical_injuries ci ON c.character_id = ci.character_id AND ci.healed = 0
WHERE c.character_id = 1
GROUP BY c.character_id;

-- Cybernetic overview with humanity impact
SELECT 
    c.handle,
    c.humanity,
    c.max_humanity,
    COUNT(cy.cybernetic_id) as implant_count,
    SUM(cy.humanity_cost) as humanity_lost
FROM characters c
LEFT JOIN cybernetics cy ON c.character_id = cy.character_id
WHERE c.character_id = 1
GROUP BY c.character_id;

-- ============================================
-- UPDATE QUERIES
-- ============================================

-- Update character HP
UPDATE characters SET hp = 35 WHERE character_id = 1;

-- Update character humanity
UPDATE characters SET humanity = 40 WHERE character_id = 1;

-- Mark injury as healed
UPDATE critical_injuries SET healed = 1 WHERE injury_id = 1;

-- Equip an item
UPDATE inventory SET equipped = 1 
WHERE character_id = 1 AND item_id = 2;

-- Unequip all items of a type
UPDATE inventory SET equipped = 0
WHERE character_id = 1 AND item_id IN (
    SELECT item_id FROM items WHERE item_type = 'weapon'
);

-- Update ammo quantity
UPDATE ammo SET quantity = quantity - 5
WHERE character_id = 1 AND ammo_type = 'Standard 9mm';

-- Mark cybernetic as malfunctioning
UPDATE cybernetics SET malfunction = 1 WHERE cybernetic_id = 1;

-- Update character last modified time
UPDATE characters SET last_modified = CURRENT_TIMESTAMP WHERE character_id = 1;

-- ============================================
-- DELETE QUERIES
-- ============================================

-- Remove item from inventory
DELETE FROM inventory WHERE character_id = 1 AND item_id = 3;

-- Delete a contact
DELETE FROM contacts WHERE contact_id = 1;

-- Remove all completed/healed critical injuries
DELETE FROM critical_injuries WHERE character_id = 1 AND healed = 1;

-- Remove inactive status effects
DELETE FROM status_effects WHERE character_id = 1 AND active = 0;

-- Delete a character (cascades to all related data)
DELETE FROM characters WHERE character_id = 1;

-- ============================================
-- STATISTICS QUERIES
-- ============================================

-- Most common character roles
SELECT role, COUNT(*) as count
FROM characters
GROUP BY role
ORDER BY count DESC;

-- Most valuable items
SELECT item_name, item_type, value
FROM items
ORDER BY value DESC
LIMIT 10;

-- Characters with most cybernetics
SELECT c.handle, COUNT(cy.cybernetic_id) as implant_count
FROM characters c
LEFT JOIN cybernetics cy ON c.character_id = cy.character_id
GROUP BY c.character_id
ORDER BY implant_count DESC;

-- Average stats across all characters
SELECT 
    AVG(intelligence) as avg_int,
    AVG(reflexes) as avg_ref,
    AVG(cool) as avg_cool,
    AVG(body) as avg_body
FROM stats;
