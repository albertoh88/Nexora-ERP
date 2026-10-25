-- Nexora ERP - esquema de base de datos (SQlite)
-- Dinero sempre em CENTAVOS (enteros). R$ 12,50 -> 1250

CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY,
    -- COLLATE NOCASE: "Papel" e "papel" são tratados como o mesmo material,
    -- tanto em comparações como em ÚNICO.
    name TEXT NOT NULL COLLATE NOCASE,
    -- Sem marca = '' (não NULL). No SQLite dois NULLs nunca são "os mesmos",
    -- é por isso que a UNIQUE (nome, marca) não evitaria duplicatas da marca NULL.
    brand TEXT NOT NULL DEFAULT '' COLLATE NOCASE,
    -- Unidade em que a quantidade é medida: ml, g, folha, a...
    unit TEXT NOT NULL DEFAULT 'un',
    -- Valor comprado e custo total pago por esse valor.
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total_cost INTEGER NOT NULL CHECK (total_cost >= 0),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),

    UNIQUE (name, brand)
);

CREATE TABLE IF NOT EXISTS cost_sheets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL COLLATE NOCASE UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1))

);

CREATE TABLE IF NOT EXISTS cost_sheets_items (
    id INTEGER PRIMARY KEY,
    cost_sheets_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    -- Quantidade de material que consome uma unidade do produto
    -- (mesma unidade que material.unit).
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    -- Custo desse valor ao adicioná-lo, em centavos:
    -- redondo (quantidade * materials.total_cost / materials.quantity)
    -- É calculado uma vez com o valor total para não perder
    -- precisão (divida primeiro a custo por unidade com centavos de perdas inteiras).
    line_cost INTEGER NOT NULL CHECK (line_cost >= 0),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (cost_sheets_id, material_id),

    FOREIGN KEY (cost_sheets_id)
        REFERENCES cost_sheets (id) ON DELETE CASCADE,

    FOREIGN KEY (material_id)
        REFERENCES materials (id) ON DELETE RESTRICT

);

-- Para responder "que fichas você usa esse material?"
CREATE INDEX IF NOT EXISTS idx_cost_sheets_items_material
    ON cost_sheets_items (material_id);
