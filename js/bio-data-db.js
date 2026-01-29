// Bio Data Management - Database Version
// Fetch and save data from/to API instead of localStorage

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';
const CHARACTER_ID = 1; // For demo, use character 1. In production, get from session/login

// Field mapping: ID in edit page -> ID in display page -> database field
const fieldMap = [
    { edit: 'handle', display: 'display-handle', db: 'handle', table: 'character' },
    { edit: 'role', display: 'display-role', db: 'role', table: 'character' },
    { edit: 'role-ability', display: 'display-role-ability', db: 'role_ability', table: 'character' },
    { edit: 'rank', display: 'display-rank', db: 'rank', table: 'character' },
    { edit: 'critical-injuries', display: 'display-critical-injuries', db: 'critical_injuries', table: 'injuries' },
    { edit: 'addictions', display: 'display-addictions', db: 'addictions', table: 'addictions' },
    { edit: 'languages', display: 'display-languages', db: 'languages', table: 'character' },
    { edit: 'family-background', display: 'display-family-background', db: 'family_background', table: 'background' },
    { edit: 'childhood-environment', display: 'display-childhood-environment', db: 'childhood_environment', table: 'background' },
    { edit: 'improvement-current', display: 'display-improvement-current', db: 'improvement_points', table: 'character' },
    { edit: 'reputation-events', display: 'display-reputation-events', db: 'reputation_event', table: 'reputation' },
    { edit: 'reputation', display: 'display-reputation', db: 'reputation_score', table: 'reputation' },
    { edit: 'cultural-region', display: 'display-cultural-region', db: 'cultural_region', table: 'character' },
    { edit: 'clothing-style', display: 'display-clothing-style', db: 'clothing_style', table: 'character' },
    { edit: 'hairstyle', display: 'display-hairstyle', db: 'hairstyle', table: 'character' },
    { edit: 'affectation', display: 'display-affectation', db: 'affectation', table: 'character' }
];

/**
 * Save bio data from edit page to database via API
 */
async function saveBioData() {
    try {
        // Show saving indicator
        console.log('Saving character data...');
        
        // Collect data from form
        const characterData = {};
        const backgroundData = {};
        const reputationData = {};
        const contactsData = {
            friends: [],
            loves: [],
            enemies: []
        };
        
        // Map basic fields
        fieldMap.forEach(field => {
            const element = document.getElementById(field.edit);
            if (element) {
                const value = element.value || '';
                
                if (field.table === 'character') {
                    characterData[field.db] = value;
                } else if (field.table === 'background') {
                    backgroundData[field.db] = value;
                } else if (field.table === 'reputation') {
                    reputationData[field.db] = value;
                }
            }
        });
        
        // Collect friends
        for (let i = 1; i <= 4; i++) {
            const friendInput = document.getElementById(`friend-${i}`);
            if (friendInput && friendInput.value.trim()) {
                contactsData.friends.push({
                    name: friendInput.value.trim(),
                    notes: ''
                });
            }
        }
        
        // Collect love interests
        for (let i = 1; i <= 4; i++) {
            const loveInput = document.getElementById(`love-${i}`);
            if (loveInput && loveInput.value.trim()) {
                contactsData.loves.push({
                    name: loveInput.value.trim(),
                    notes: ''
                });
            }
        }
        
        // Collect enemies
        for (let i = 1; i <= 3; i++) {
            const whoInput = document.getElementById(`enemy-${i}-who`);
            const causedInput = document.getElementById(`enemy-${i}-caused`);
            const throwInput = document.getElementById(`enemy-${i}-throw`);
            const happenInput = document.getElementById(`enemy-${i}-happen`);
            
            if (whoInput && whoInput.value.trim()) {
                contactsData.enemies.push({
                    name: whoInput.value.trim(),
                    who_wronged: whoInput.value.trim(),
                    what_caused: causedInput ? causedInput.value.trim() : '',
                    what_throw_down: throwInput ? throwInput.value.trim() : '',
                    what_happened: happenInput ? happenInput.value.trim() : '',
                    notes: ''
                });
            }
        }
        
        // Collect critical injuries
        const injuriesInput = document.getElementById('critical-injuries');
        const critical_injuries = injuriesInput ? injuriesInput.value : '';
        
        // Collect addictions
        const addictionsInput = document.getElementById('addictions');
        const addictions = addictionsInput ? addictionsInput.value : '';
        
        // Build request payload
        const payload = {
            character: characterData,
            background: backgroundData,
            contacts: contactsData,
            reputation: reputationData,
            critical_injuries: critical_injuries,
            addictions: addictions
        };
        
        // Send to API
        const response = await fetch(`${API_BASE_URL}/character/${CHARACTER_ID}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Character data saved successfully!', result);
        
        // Navigate back to display page
        loadBioPage('bio.html');
        
    } catch (error) {
        console.error('Error saving character data:', error);
        alert('Failed to save character data. Make sure the API server is running.\n\nTo start the server:\n  cd api\n  python3 app.py');
    }
}

/**
 * Load bio data from database to edit page
 */
async function loadBioDataToEdit() {
    try {
        console.log('Loading character data for editing...');
        
        const response = await fetch(`${API_BASE_URL}/character/${CHARACTER_ID}`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Loaded character data:', data);
        
        // Populate basic fields
        fieldMap.forEach(field => {
            const element = document.getElementById(field.edit);
            if (element) {
                let value = '';
                
                if (field.table === 'character') {
                    value = data.character[field.db] || '';
                } else if (field.table === 'background') {
                    value = data.background[field.db] || '';
                } else if (field.table === 'reputation') {
                    value = data.reputation[field.db] || '';
                }
                
                element.value = value;
            }
        });
        
        // Populate friends
        data.contacts.friends.forEach((friend, index) => {
            const friendInput = document.getElementById(`friend-${index + 1}`);
            if (friendInput) {
                friendInput.value = friend.name;
            }
        });
        
        // Populate love interests
        data.contacts.loves.forEach((love, index) => {
            const loveInput = document.getElementById(`love-${index + 1}`);
            if (loveInput) {
                loveInput.value = love.name;
            }
        });
        
        // Populate enemies
        data.contacts.enemies.forEach((enemy, index) => {
            const whoInput = document.getElementById(`enemy-${index + 1}-who`);
            const causedInput = document.getElementById(`enemy-${index + 1}-caused`);
            const throwInput = document.getElementById(`enemy-${index + 1}-throw`);
            const happenInput = document.getElementById(`enemy-${index + 1}-happen`);
            
            if (whoInput) whoInput.value = enemy.name;
            if (causedInput) causedInput.value = enemy.what_caused || '';
            if (throwInput) throwInput.value = enemy.what_throw_down || '';
            if (happenInput) happenInput.value = enemy.what_happened || '';
        });
        
        // Populate critical injuries
        const injuriesInput = document.getElementById('critical-injuries');
        if (injuriesInput && data.critical_injuries.length > 0) {
            injuriesInput.value = data.critical_injuries.map(i => i.description || i.injury_name).join('\n');
        }
        
        // Populate addictions
        const addictionsInput = document.getElementById('addictions');
        if (addictionsInput && data.addictions.length > 0) {
            addictionsInput.value = data.addictions.map(a => a.substance).join('\n');
        }
        
    } catch (error) {
        console.error('Error loading character data:', error);
        console.log('Falling back to empty form. Make sure API server is running.');
    }
}

/**
 * Load bio data from database to display page
 */
async function loadBioDataToDisplay() {
    try {
        console.log('Loading character data for display...');
        
        const response = await fetch(`${API_BASE_URL}/character/${CHARACTER_ID}`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Loaded character data:', data);
        
        // Populate basic fields
        fieldMap.forEach(field => {
            const element = document.getElementById(field.display);
            if (element) {
                let value = '';
                
                if (field.table === 'character') {
                    value = data.character[field.db] || '';
                } else if (field.table === 'background') {
                    value = data.background[field.db] || '';
                } else if (field.table === 'reputation') {
                    value = data.reputation[field.db] || '';
                }
                
                element.textContent = value;
            }
        });
        
        // Populate friends
        data.contacts.friends.forEach((friend, index) => {
            const friendElement = document.getElementById(`display-friend-${index + 1}`);
            if (friendElement) {
                friendElement.textContent = friend.name;
            }
        });
        
        // Populate love interests
        data.contacts.loves.forEach((love, index) => {
            const loveElement = document.getElementById(`display-love-${index + 1}`);
            if (loveElement) {
                loveElement.textContent = love.name;
            }
        });
        
        // Populate enemies
        data.contacts.enemies.forEach((enemy, index) => {
            const whoElement = document.getElementById(`display-enemy-${index + 1}-who`);
            const causedElement = document.getElementById(`display-enemy-${index + 1}-caused`);
            const throwElement = document.getElementById(`display-enemy-${index + 1}-throw`);
            const happenElement = document.getElementById(`display-enemy-${index + 1}-happen`);
            
            if (whoElement) whoElement.textContent = enemy.name;
            if (causedElement) causedElement.textContent = enemy.what_caused || '';
            if (throwElement) throwElement.textContent = enemy.what_throw_down || '';
            if (happenElement) happenElement.textContent = enemy.what_happened || '';
        });
        
        // Populate critical injuries
        const injuriesElement = document.getElementById('display-critical-injuries');
        if (injuriesElement && data.critical_injuries.length > 0) {
            injuriesElement.textContent = data.critical_injuries.map(i => i.description || i.injury_name).join('\n');
        }
        
        // Populate addictions
        const addictionsElement = document.getElementById('display-addictions');
        if (addictionsElement && data.addictions.length > 0) {
            addictionsElement.textContent = data.addictions.map(a => a.substance).join('\n');
        }
        
    } catch (error) {
        console.error('Error loading character data:', error);
        console.log('Make sure API server is running.');
    }
}

// Make functions available globally
window.saveBioData = saveBioData;
window.loadBioDataToEdit = loadBioDataToEdit;
window.loadBioDataToDisplay = loadBioDataToDisplay;
