CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    brand TEXT,
    quantity INTEGER NOT NULL,
    total_cost INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),

    UNIQUE (name, brand)
);

CREATE TABLE IF NOT EXISTS cost_sheets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1))

);

CREATE TABLE IF NOT EXISTS cost_sheets_items (
    id INTEGER PRIMARY KEY,
    cost_sheets_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_cost INTEGER NOT NULL,
    created_at DATETIME,

    UNIQUE (cost_sheets_id, material_id),

    FOREIGN KEY (cost_sheets_id)
        REFERENCES cost_sheets (id),

    FOREIGN KEY (material_id)
        REFERENCES materials (id)

);

