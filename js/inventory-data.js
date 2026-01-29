// Inventory data with Finnish translations
const inventoryData = {
    all: {
        name: "Kaikki",
        items: []
    },
    weapons: {
        name: "Aseet & Ammo",
        items: [
            {
                id: "weapon-1",
                name: "Katakana asetta",
                description: "Tehokas rinnakkain ampuja",
                value: 1500,
                quantity: 1
            },
            {
                id: "weapon-2",
                name: "Pulssariifle",
                description: "Energiaseikka vaikutus",
                value: 3200,
                quantity: 2
            }
        ]
    },
    vehicles: {
        name: "Ajoneuvot",
        items: [
            {
                id: "vehicle-1",
                name: "Ajoneuvo - Jalokivi Ground",
                description: "Nopea ja väärä maastoajoneuvon",
                value: 45000,
                quantity: 1
            },
            {
                id: "vehicle-2",
                name: "Ilmakulkuneuvo - Air ja Sea",
                description: "Amphibious ajoneuvon monipuolinen liikutteluun",
                value: 75000,
                quantity: 1
            }
        ]
    },
    equipment: {
        name: "Varusteet",
        items: [
            {
                id: "equipment-1",
                name: "Pansari, vaatteet",
                description: "Suojava varuste",
                value: 2500,
                quantity: 3
            },
            {
                id: "equipment-2",
                name: "Turvalaitteet",
                description: "Ammus-, väliaine- ja kuorinsuojaksi",
                value: 1800,
                quantity: 2
            }
        ]
    },
    cyberware: {
        name: "Kyberware",
        items: [
            {
                id: "cyberware-1",
                name: "Kyberware - Pään sisäosa",
                description: "Neurologiset parannukset",
                value: 5000,
                quantity: 1
            },
            {
                id: "cyberware-2",
                name: "Kyberware - Käsi",
                description: "Käden parannetut toiminnot",
                value: 4200,
                quantity: 1
            },
            {
                id: "cyberware-3",
                name: "Kyberware - Silmä, sisäinen",
                description: "Näön parantaminen kyberneettisesti",
                value: 3500,
                quantity: 1
            }
        ]
    },
    misc: {
        name: "Muuta",
        items: [
            {
                id: "misc-1",
                name: "Kaikki misc tavarat",
                description: "Sekalainen kokoelma",
                value: 800,
                quantity: 5
            }
        ]
    }
};

// Populate "all" category with items from all other categories
Object.keys(inventoryData).forEach(category => {
    if (category !== 'all') {
        inventoryData.all.items.push(...inventoryData[category].items);
    }
});

function initializeInventory() {
    // Get all category buttons
    const categoryButtons = document.querySelectorAll(".inventory-category-btn");
    const inventorySections = document.querySelectorAll(".inventory-section");
    const inventoryItems = document.querySelectorAll(".inventory-item");

    // Category button click handlers
    categoryButtons.forEach(button => {
        button.addEventListener("click", () => {
            const category = button.dataset.category;

            // Update active button
            categoryButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            // Update visible section
            inventorySections.forEach(section => section.classList.add("hidden"));
            const sectionId = category + "-section";
            const section = document.getElementById(sectionId);
            if (section) {
                section.classList.remove("hidden");
            }
        });
    });

    // Item click handlers - set up delegation
    const centerPanel = document.querySelector(".inventory-center-panel");
    if (centerPanel) {
        centerPanel.addEventListener("click", (e) => {
            const itemElement = e.target.closest(".inventory-item");
            if (itemElement) {
                selectItem(itemElement);
            }
        });
    }
}

function selectItem(itemElement) {
    // Remove previous selection
    document.querySelectorAll(".inventory-item").forEach(item => {
        item.classList.remove("selected");
    });

    // Mark this item as selected
    itemElement.classList.add("selected");

    // Get item ID and find the data
    const itemId = itemElement.dataset.itemId;
    let itemData = null;

    // Search for item in inventory data
    Object.keys(inventoryData).forEach(category => {
        const foundItem = inventoryData[category].items.find(item => item.id === itemId);
        if (foundItem) {
            itemData = foundItem;
        }
    });

    // Update right panel with item info
    if (itemData) {
        document.getElementById("info-name").textContent = itemData.name;
        document.getElementById("info-description").textContent = itemData.description;
        document.getElementById("info-value").textContent = itemData.value + " EB";
        document.getElementById("info-quantity").textContent = itemData.quantity + "";
    }
}

// Make functions globally available
window.initializeInventory = initializeInventory;
window.selectItem = selectItem;
