CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    stats TEXT,
    inventory TEXT,
    actions TEXT
);

CREATE TABLE campaign_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    narrative TEXT,
    encounters TEXT,
    npcs TEXT
);

CREATE TABLE maps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    data TEXT
);
