document.addEventListener("DOMContentLoaded", () => {
    const mapContainer = document.getElementById("map");
    const tokenContainer = document.getElementById("tokens");

    // Initialize the map
    function initializeMap() {
        // Load map background
        mapContainer.style.backgroundImage = "url('/static/images/map_placeholder.jpg')";
        mapContainer.style.backgroundSize = "contain";
        mapContainer.style.backgroundRepeat = "no-repeat";
        mapContainer.style.width = "800px";
        mapContainer.style.height = "600px";
        mapContainer.style.position = "relative"; // Needed for absolute positioning of tokens
    }
    function snapToGrid(value, gridSize) {
        return Math.round(value / gridSize) * gridSize;
    }
    
    function dragEnd(event) {
        const token = document.getElementById(event.target.id);
        const x = event.pageX - mapContainer.offsetLeft;
        const y = event.pageY - mapContainer.offsetTop;
    
        // Snap to a 50px grid
        token.style.left = `${snapToGrid(x, 50)}px`;
        token.style.top = `${snapToGrid(y, 50)}px`;
    }
    
    // Function to add a token to the map
    function addToken(filename, x = 50, y = 50) {
        const token = document.createElement("img");
        token.src = `/static/images/tokens/${filename}`;
        token.style.width = "40px";
        token.style.height = "40px";
        token.style.position = "absolute";
        token.style.left = `${x}px`;
        token.style.top = `${y}px`;
        token.style.cursor = "pointer";
        token.draggable = true;

        // Add dragging events
        token.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("text/plain", filename);
            token.style.zIndex = "1000"; // Bring token to the front during dragging
        });

        token.addEventListener("dragend", (e) => {
            const rect = mapContainer.getBoundingClientRect();
            const x = e.pageX - rect.left; // Adjust relative to the map
            const y = e.pageY - rect.top;

            token.style.left = `${x}px`;
            token.style.top = `${y}px`;
            token.style.zIndex = "10"; // Reset z-index after dragging
        });

        mapContainer.appendChild(token);
    }
    // Example: Call `addToken` after a successful token upload
    document.getElementById("tokenForm").addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
    
        fetch("/upload-token", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addToken(data.filename); // Pass uploaded token's filename
                    alert(data.message);
                } else {
                    alert("Failed to upload token.");
                }
            })
            .catch(error => console.error("Error:", error));
    });
    
    

    // Dragging events
    function dragStart(event) {
        event.dataTransfer.setData("text/plain", event.target.id);
    }

    function dragEnd(event) {
        const token = document.getElementById(event.target.id);
        token.style.left = `${event.pageX - mapContainer.offsetLeft}px`;
        token.style.top = `${event.pageY - mapContainer.offsetTop}px`;
    }

    function updateMap(filename) {
        const mapContainer = document.getElementById("map");
        mapContainer.style.backgroundImage = `url('/maps/${filename}')`;
    }

    document.addEventListener("DOMContentLoaded", () => {
        const mapContainer = document.getElementById("map");
    
        // Load uploaded map dynamically
        function loadMap() {
            fetch('/static/images/map_placeholder.jpg') // Adjust this URL if needed
                .then(response => {
                    if (response.ok) {
                        mapContainer.style.backgroundImage = "url('/static/images/map_placeholder.jpg')";
                        mapContainer.style.backgroundSize = "contain";
                        mapContainer.style.width = "800px";
                        mapContainer.style.height = "600px";
                        mapContainer.style.border = "1px solid black";
                        mapContainer.style.margin = "20px auto";
                    }
                })
                .catch(error => console.error("Error loading map:", error));
        }
    
        loadMap();
    });
    
    function updateMap(filename) {
        const mapContainer = document.getElementById("map");
        mapContainer.style.backgroundImage = `url('/app/maps/${filename}')`; // Ensure filename points to the uploaded map
    }
    
    // Example: Call `updateMap` after a successful upload
    document.getElementById("uploadForm").addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
    
        fetch("/upload-map", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateMap(data.filename); // Pass uploaded map's filename
                    alert(data.message);
                } else {
                    alert("Failed to upload map.");
                }
            })
            .catch(error => console.error("Error:", error));
    });
    
    
    // Initialize the map when the page loads
    initializeMap();

    // Example: Add some tokens for testing
    addToken(1, 100, 150); // Token 1 at x=100, y=150
    addToken(2, 300, 400); // Token 2 at x=300, y=400
});
