DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL, -- Citizen, Shelter Admin, Rescue Team, System Admin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rescue_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    location TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    details TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending', -- Pending, In Progress, Resolved, Canceled
    priority TEXT NOT NULL DEFAULT 'Medium', -- Low, Medium, High, Critical
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS shelters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    current_occupancy INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'Open', -- Open, Full, Closed
    latitude REAL,
    longitude REAL
);

-- Seed data for testing recommendations
INSERT INTO shelters (name, location, capacity, current_occupancy, status, latitude, longitude) VALUES 
('Downtown Safe Haven', '100 Broadway St, Downtown', 150, 45, 'Open', 23.812, 90.415),
('Northside Community Center', '450 Oak Ave, Northside', 80, 78, 'Open', 23.830, 90.410),
('Eastside Gymnasium', '789 Maple Rd, Eastside', 200, 195, 'Open', 23.805, 90.435),
('Westside Secondary School', '101 Pine Blvd, Westside', 120, 0, 'Open', 23.815, 90.395);

CREATE TABLE IF NOT EXISTS disaster_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'Watch', -- Watch, Warning, Critical
    area TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(created_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL, -- Food, Water, Medicine, Equipment, Clothing
    quantity INTEGER NOT NULL DEFAULT 0,
    unit TEXT NOT NULL DEFAULT 'units',
    shelter_id INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(shelter_id) REFERENCES shelters(id)
);

-- Seed resource data
INSERT INTO disaster_alerts (title, description, severity, area, is_active) VALUES
('Flash Flood Warning', 'Heavy rainfall expected. Low-lying areas should evacuate immediately.', 'Critical', 'Downtown & Eastside', 1),
('Storm Watch', 'Tropical storm approaching. Secure loose outdoor items.', 'Watch', 'Coastal Areas', 1);

INSERT INTO resources (name, category, quantity, unit, shelter_id) VALUES
('Drinking Water', 'Water', 500, 'liters', 1),
('Emergency Food Packs', 'Food', 200, 'packs', 1),
('First Aid Kits', 'Medicine', 50, 'kits', 2),
('Blankets', 'Clothing', 150, 'pieces', 1),
('Generators', 'Equipment', 5, 'units', 3);
