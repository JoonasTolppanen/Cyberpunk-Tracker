// Bio Data Management - Save and Load Functions

// Field mapping: ID in edit page -> ID in display page
const fieldMap = [
    { edit: 'handle', display: 'display-handle' },
    { edit: 'role', display: 'display-role' },
    { edit: 'role-ability', display: 'display-role-ability' },
    { edit: 'rank', display: 'display-rank' },
    { edit: 'ability', display: 'display-ability' },
    { edit: 'critical-injuries', display: 'display-critical-injuries' },
    { edit: 'addictions', display: 'display-addictions' },
    { edit: 'languages', display: 'display-languages' },
    { edit: 'family-background', display: 'display-family-background' },
    { edit: 'childhood-environment', display: 'display-childhood-environment' },
    { edit: 'friend-1', display: 'display-friend-1' },
    { edit: 'friend-2', display: 'display-friend-2' },
    { edit: 'friend-3', display: 'display-friend-3' },
    { edit: 'friend-4', display: 'display-friend-4' },
    { edit: 'love-1', display: 'display-love-1' },
    { edit: 'love-2', display: 'display-love-2' },
    { edit: 'love-3', display: 'display-love-3' },
    { edit: 'love-4', display: 'display-love-4' },
    { edit: 'enemy-1-who', display: 'display-enemy-1-who' },
    { edit: 'enemy-1-caused', display: 'display-enemy-1-caused' },
    { edit: 'enemy-1-throw', display: 'display-enemy-1-throw' },
    { edit: 'enemy-1-happen', display: 'display-enemy-1-happen' },
    { edit: 'enemy-2-who', display: 'display-enemy-2-who' },
    { edit: 'enemy-2-caused', display: 'display-enemy-2-caused' },
    { edit: 'enemy-2-throw', display: 'display-enemy-2-throw' },
    { edit: 'enemy-2-happen', display: 'display-enemy-2-happen' },
    { edit: 'enemy-3-who', display: 'display-enemy-3-who' },
    { edit: 'enemy-3-caused', display: 'display-enemy-3-caused' },
    { edit: 'enemy-3-throw', display: 'display-enemy-3-throw' },
    { edit: 'enemy-3-happen', display: 'display-enemy-3-happen' },
    { edit: 'improvement-current', display: 'display-improvement-current' },
    { edit: 'improvement-outof', display: 'display-improvement-outof' },
    { edit: 'reputation', display: 'display-reputation' },
    { edit: 'cultural-region', display: 'display-cultural-region' },
    { edit: 'clothing-style', display: 'display-clothing-style' },
    { edit: 'hairstyle', display: 'display-hairstyle' },
    { edit: 'affectation', display: 'display-affectation' }
];

// Save bio data from edit page to localStorage
function saveBioData() {
    const bioData = {};
    
    // Collect all field values
    fieldMap.forEach(field => {
        const element = document.getElementById(field.edit);
        if (element) {
            bioData[field.edit] = element.value || '';
        }
    });
    
    // Save to localStorage
    localStorage.setItem('cyberpunk-bio-data', JSON.stringify(bioData));
    
    // Show feedback (optional)
    console.log('Bio data saved!');
    
    // Navigate back to display page
    loadBioPage('bio.html');
}

// Load bio data from localStorage to edit page
function loadBioDataToEdit() {
    const savedData = localStorage.getItem('cyberpunk-bio-data');
    
    if (savedData) {
        const bioData = JSON.parse(savedData);
        
        // Populate all fields
        fieldMap.forEach(field => {
            const element = document.getElementById(field.edit);
            if (element && bioData[field.edit] !== undefined) {
                element.value = bioData[field.edit];
            }
        });
    }
}

// Load bio data from localStorage to display page
function loadBioDataToDisplay() {
    const savedData = localStorage.getItem('cyberpunk-bio-data');
    
    if (savedData) {
        const bioData = JSON.parse(savedData);
        
        // Populate all display fields
        fieldMap.forEach(field => {
            const element = document.getElementById(field.display);
            if (element && bioData[field.edit] !== undefined) {
                element.textContent = bioData[field.edit];
            }
        });
    }
}

// Make functions available globally
window.saveBioData = saveBioData;
window.loadBioDataToEdit = loadBioDataToEdit;
window.loadBioDataToDisplay = loadBioDataToDisplay;
