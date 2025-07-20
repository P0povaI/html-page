document.addEventListener('DOMContentLoaded', () => {
    // State Variables
    let currentPlayerState = null;
    let currentRoomData = null;
    let currentEnemyData = null;

    // --- DOM Elements ---
    const startScreen = document.getElementById('start-screen');
    const gameScreen = document.getElementById('game-screen');
    const gameOverScreen = document.getElementById('game-over-screen');
    const gameCompleteScreen = document.getElementById('game-complete-screen');

    const playerNameInput = document.getElementById('player-name-input');
    const startGameButton = document.getElementById('start-game-button');
    
    // Player Stats
    const playerNameDisplay = document.getElementById('player-name');
    const playerHealthDisplay = document.getElementById('player-health');
    const playerXpDisplay = document.getElementById('player-xp');
    const playerLevelDisplay = document.getElementById('player-level');
    const playerCoinsDisplay = document.getElementById('player-coins');
    const playerKillsDisplay = document.getElementById('player-kills');
    const playerEffectBleeding = document.getElementById('player-effect-bleeding');
    const playerEffectCursed = document.getElementById('player-effect-cursed');

    // Room Area
    const roomImage = document.getElementById('room-image');
    const roomImagePlaceholder = document.getElementById('room-image-placeholder');
    const roomDescriptionDisplay = document.getElementById('room-description');
    const storyContentDisplay = document.getElementById('story-content');

    // Action Area
    const actionResultDisplay = document.getElementById('action-result');
    const actionButtonsContainer = document.getElementById('action-buttons');
    const nextRoomButton = document.getElementById('next-room-button');
    
    // --- Utility Functions ---
    function showElement(element) {
        element.classList.remove('hidden');
    }

    function hideElement(element) {
        element.classList.add('hidden');
    }

    function clearChildren(element) {
        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }
    }

    // --- Core Game Logic ---
    async function initGame() {
        const playerName = playerNameInput.value.trim();
        if (!playerName) {
            alert("Please enter a name for your adventurer!");
            return;
        }

        try {
            const response = await fetch('/game/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: playerName })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            
            currentPlayerState = data.player;
            
            hideElement(startScreen);
            showElement(gameScreen);
            
            updatePlayerStatsUI();
            processRoomData(data.room);

        } catch (error) {
            console.error("Error starting game:", error);
            alert("Failed to start the game. Is the server running? Please check the console for errors.");
        }
    }

    function updatePlayerStatsUI() {
        if (!currentPlayerState) return;

        playerNameDisplay.innerHTML = `<span class="emoji">👤</span> ${currentPlayerState.name}`;
        playerHealthDisplay.innerHTML = `<span class="emoji">🧡</span> ${currentPlayerState.health}/${currentPlayerState.max_health}`;
        playerXpDisplay.innerHTML = `<span class="emoji">🧠</span> ${currentPlayerState.experience}`;
        playerLevelDisplay.innerHTML = `<span class="emoji">🎓</span> Level ${currentPlayerState.level}`;
        playerCoinsDisplay.innerHTML = `<span class="emoji">💰</span> ${currentPlayerState.coins} Coins`;
        playerKillsDisplay.innerHTML = `<span class="emoji">💀</span> ${currentPlayerState.kills} Kills`;

        // Update status effect icons
        if (currentPlayerState.is_bleeding) {
            showElement(playerEffectBleeding);
        } else {
            hideElement(playerEffectBleeding);
        }

        if (currentPlayerState.is_cursed) {
            showElement(playerEffectCursed);
        } else {
            hideElement(playerEffectCursed);
        }

        // Check for game over condition
        if (currentPlayerState.health <= 0) {
            handleGameOver();
        }
    }
    
    async function processRoomData(roomData) {
        currentRoomData = roomData;
        currentEnemyData = null; // Reset enemy data for new room

        // Update UI
        roomDescriptionDisplay.textContent = roomData.room_description;
        actionResultDisplay.textContent = ''; // Clear previous results
        hideElement(actionResultDisplay); // Ensure the result box is hidden on new room
        hideElement(nextRoomButton);
        clearChildren(actionButtonsContainer);
        hideElement(storyContentDisplay);

        // Create action buttons and handle images based on room type
        switch (roomData.room_type) {
            case "Story":
                hideElement(roomImage);
                hideElement(roomImagePlaceholder);
                // For story rooms, display the narrative in the main action result area for prominence.
                roomDescriptionDisplay.textContent = "A new chapter of your story unfolds...";
                actionResultDisplay.innerHTML = roomData.room_description.replace(/\n/g, '<br>');
                showElement(actionResultDisplay); // Make sure it's visible
                showElement(nextRoomButton); // Story rooms just lead to the next room
                break;
            case "Fight":
                try {
                    const response = await fetch('/enemy');
                    if (!response.ok) throw new Error("Failed to get enemy");
                    currentEnemyData = await response.json();
                    
                    // Set image based on enemy class
                    setRoomImage(currentEnemyData.enemy_class); // Will be 'mage' or 'fighter'
                    
                    // Construct a single, clean description on the frontend
                    roomDescriptionDisplay.textContent = `A ${currentEnemyData.enemy_type} ${currentEnemyData.enemy_class} with ${currentEnemyData.health} HP appears and attacks you!`;

                    createButton("Attack", () => handleAction('fight/attack'));
                    createButton("Run", () => handleAction('fight/run'));
                } catch (error) {
                    console.error("Error fetching enemy:", error);
                    setRoomImage('fighter'); // Fallback image
                    actionResultDisplay.textContent = "An enemy was supposed to be here, but it seems to have vanished. You can proceed.";
                    showElement(actionResultDisplay);
                    showElement(nextRoomButton);
                }
                break;
            case "Chest":
                setRoomImage('chest');
                createButton("Open Chest", () => handleAction('chest/open'));
                createButton("Skip", () => handleNextRoom());
                break;
            case "Shop":
                setRoomImage('shop');
                // Fetch the catalog and dynamically create buttons
                fetch('/marketplace/catalog')
                    .then(response => {
                        if (!response.ok) throw new Error("Shop is closed");
                        return response.json();
                    })
                    .then(catalog => {
                        for (const [itemId, cost] of Object.entries(catalog)) {
                            // Format the item name for display
                            const itemName = itemId.replace(/_/g, ' ');
                            const buttonText = `Buy ${itemName} (${cost} 💰)`;
                            const button = createButton(buttonText, () => handleAction('marketplace/purchase', { item: itemId }));

                            if (currentPlayerState.coins < cost) {
                                button.disabled = true;
                                button.title = "Not enough coins!";
                                button.style.cursor = 'not-allowed';
                                button.style.backgroundColor = '#444'; // Darken disabled button
                            }
                        }
                        // Always add a leave button
                        createButton("Leave Shop", () => handleNextRoom());
                    })
                    .catch(error => {
                        console.error("Error fetching marketplace catalog:", error);
                        actionResultDisplay.textContent = "The shop seems to be closed today. You can proceed.";
                        showElement(actionResultDisplay);
                        showElement(nextRoomButton);
                    });
                break;
            case "Casino":
                setRoomImage('casino');
                
                // Container for the betting UI
                const betUiContainer = document.createElement('div');
                betUiContainer.style.display = 'flex';
                betUiContainer.style.gap = '10px';
                betUiContainer.style.alignItems = 'center';
                betUiContainer.style.marginBottom = '10px'; // Space between this and Leave button

                // Input field for the bet amount
                const betInput = document.createElement('input');
                betInput.type = 'number';
                betInput.placeholder = `Max bet: ${currentPlayerState.coins}`;
                betInput.min = '1';
                betInput.max = currentPlayerState.coins.toString();
                betInput.style.fontFamily = 'var(--font-family)';
                betInput.style.padding = '10px';
                betInput.style.backgroundColor = 'var(--primary-bg)';
                betInput.style.color = 'var(--text-color)';
                betInput.style.border = '1px solid var(--border-color)';
                betInput.style.width = '100%';

                // The "Place Bet" button
                const placeBetButton = document.createElement('button');
                placeBetButton.textContent = 'Bet';
                // Override the default 100% width from CSS
                placeBetButton.style.width = 'auto'; 
                placeBetButton.addEventListener('click', () => {
                    const betAmount = parseInt(betInput.value, 10);

                    if (isNaN(betAmount) || betAmount <= 0) {
                        alert("Please enter a valid, positive amount to bet.");
                        return;
                    }
                    if (betAmount > currentPlayerState.coins) {
                        alert(`You can't bet more than you have! Your max bet is ${currentPlayerState.coins} 💰.`);
                        return;
                    }
                    handleAction('casino/bet', { bet: betAmount });
                });

                betUiContainer.appendChild(betInput);
                betUiContainer.appendChild(placeBetButton);
                actionButtonsContainer.appendChild(betUiContainer);

                // Disable betting controls if player has no coins
                if (currentPlayerState.coins <= 0) {
                    betInput.disabled = true;
                    placeBetButton.disabled = true;
                    betInput.placeholder = "You have no coins!";
                    placeBetButton.style.cursor = 'not-allowed';
                    placeBetButton.style.backgroundColor = '#444';
                    placeBetButton.title = "You have no coins to bet.";
                }
                
                // Add the leave button separately, it will appear below the bet UI
                createButton("Leave Casino", () => handleNextRoom());
                break;
            case "Bedroom":
                setRoomImage('bedroom');
                fetch('/bedroom/options')
                    .then(response => {
                        if (!response.ok) throw new Error("Bedroom is unavailable");
                        return response.json();
                    })
                    .then(options => {
                        const sleepCost = options.sleep;
                        const sleepButton = createButton(`Sleep (${sleepCost} 💰)`, () => handleAction('bedroom/sleep'));

                        if (currentPlayerState.coins < sleepCost) {
                            sleepButton.disabled = true;
                            sleepButton.title = "Not enough coins!";
                            sleepButton.style.cursor = 'not-allowed';
                            sleepButton.style.backgroundColor = '#444';
                        }

                        createButton("Skip", () => handleNextRoom());
                    })
                    .catch(error => {
                        console.error("Error fetching bedroom options:", error);
                        actionResultDisplay.textContent = "The innkeeper seems to be away. You can proceed.";
                        showElement(actionResultDisplay);
                        showElement(nextRoomButton);
                    });
                break;
            default:
                hideElement(roomImage);
                showElement(roomImagePlaceholder);
                roomImagePlaceholder.textContent = `Image for "${roomData.room_type}" not found.`;
                // If room type is unknown, just allow moving to the next room
                showElement(nextRoomButton);
        }
    }

    function setRoomImage(imageName) {
        if (!imageName) {
            hideElement(roomImage);
            showElement(roomImagePlaceholder);
            roomImagePlaceholder.textContent = `No image specified.`;
            return;
        }
        const imageUrl = `/static_assets/${imageName.toLowerCase()}.png`;
        
        const img = new Image();
        img.onload = () => {
            roomImage.src = imageUrl;
            showElement(roomImage);
            hideElement(roomImagePlaceholder);
        };
        img.onerror = () => {
            hideElement(roomImage);
            showElement(roomImagePlaceholder);
            roomImagePlaceholder.textContent = `Image for "${imageName}" not found.`;
        };
        img.src = imageUrl;
    }

    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function displayLogWithDelay(logText) {
        const lines = logText.split('\n').filter(line => line.trim() !== ''); // Split and remove empty lines
        for (const line of lines) {
            actionResultDisplay.innerHTML += line + '<br>';
            // Auto-scroll to the bottom of the action result box
            actionResultDisplay.scrollTop = actionResultDisplay.scrollHeight;
            await delay(1000); // Wait 1 second
        }
    }

    function createButton(text, onClick) {
        const button = document.createElement('button');
        button.textContent = text;
        button.addEventListener('click', onClick);
        actionButtonsContainer.appendChild(button);
        return button; // Return the created button
    }

    async function handleAction(endpoint, body = {}) {
        if (!currentPlayerState) return;

        // Immediately clear action buttons to prevent multiple clicks
        clearChildren(actionButtonsContainer);

        // Base body always includes player state
        const requestBody = {
            player: currentPlayerState,
            ...body
        };
        
        // Special case for fight actions that need enemy data
        if (endpoint.startsWith('fight/')) {
            requestBody.enemy = currentEnemyData;
        }

        try {
            const response = await fetch(`/actions/${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            
            // If it's a fight, display the log with a delay. Otherwise, show it instantly.
            if (endpoint.startsWith('fight/')) {
                actionResultDisplay.innerHTML = ''; // Clear for new log
                showElement(actionResultDisplay);
                await displayLogWithDelay(data.result);
            } else {
                actionResultDisplay.innerHTML = data.result.replace(/\n/g, '<br>');
                showElement(actionResultDisplay);
            }

            // Update player state with the final state from the server *after* the log is displayed
            currentPlayerState = data.player;
            updatePlayerStatsUI(); // This will trigger handleGameOver if health is <= 0

            // Only show the "Next Room" button if the player is alive.
            if (currentPlayerState.health > 0) {
                showElement(nextRoomButton);
            }

        } catch (error) {
            console.error(`Error during action ${endpoint}:`, error);
            actionResultDisplay.textContent = "An error occurred. Please try again.";
            showElement(actionResultDisplay);
            showElement(nextRoomButton); // Show next room button on error so player isn't stuck
        }
    }

    async function handleNextRoom() {
        try {
            const response = await fetch('/game/next_room');
            if (!response.ok) {
                throw new Error("Failed to fetch the next room.");
            }
            const roomData = await response.json();
            processRoomData(roomData);
        } catch(error) {
            console.error("Error fetching next room:", error);
            actionResultDisplay.textContent = "The path forward is blocked. Try again.";
        }
    }
    
    function handleGameOver() {
        const finalStats = `Final Stats - Level: ${currentPlayerState.level}, Kills: ${currentPlayerState.kills}, Coins: ${currentPlayerState.coins}.`;
        const gameOverMessage = document.querySelector('#game-over-screen p');
        
        // Use the last action's result as the death message, or a generic one.
        const deathMessage = actionResultDisplay.innerHTML || "You have been defeated.";
        
        gameOverMessage.innerHTML = `${deathMessage}<br><br>${finalStats}`;

        hideElement(gameScreen);
        showElement(gameOverScreen);
    }

    // --- Event Listeners ---
    const restartGameButton = document.getElementById('restart-game-button');

    startGameButton.addEventListener('click', initGame);
    nextRoomButton.addEventListener('click', handleNextRoom);
    restartGameButton.addEventListener('click', () => {
        // Simple reload to restart the game from scratch
        window.location.reload();
    });

    // Optional: Allow pressing Enter to start the game
    playerNameInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            initGame();
        }
    });
}); 