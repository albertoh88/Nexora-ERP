# Execute o SQL correspondente

import sqlite3
from contextlib import closing

from database import connection

class MaterialRepository:

    """Acesso à tabela `materiais`.

    Convenção: `marca` chega sempre como texto ("" se não houver marca),
    Nunca como nenhum. Então `marca = ? ` funciona e o ÚNICO (nome, marca)
    da tabela também (em SQLite, dois NULLs nunca são considerados iguais)."""

    def insert_material(self, name, brand, quantity, total_cost):
        try:
            # `with conn` faz commit se tudo correr bem e rollback se houver erro
            with closing(connection.get_connection()) as conn, conn:

                conn.execute("""INSERT INTO materials (name, brand, quantity, total_cost) VALUES (?, ?, ?, ?)""", (name, brand, quantity, total_cost))

                return True
        except sqlite3.IntegrityError as e:
            raise ValueError("A material with this name and brand already exists.") from e
        except sqlite3.Error as e:
            raise RuntimeError(f"Error while inserting the material: {e}") from e

    def update_material(self, name, brand, quantity, total_cost):
        try:
            with closing(connection.get_connection()) as conn, conn:
                cursor = conn.execute("""UPDATE materials SET quantity = ?, total_cost = ?, updated_at = CURRENT_TIMESTAMP WHERE name = ? COLLATE NOCASE AND brand = ? COLLATE NOCASE""", (quantity, total_cost, name, brand))
                if cursor.rowcount == 0:
                    raise ValueError("Material not found.")
            return True
        except sqlite3.Error as e:
            raise RuntimeError(f"Error while updating the material: {e}") from e

    def get_by_name(self, name, brand):
        """Retorne o material como um ditado, ou nenhum se ele não existe."""
        try:
            with closing(connection.get_connection()) as conn:
                row = conn.execute("SELECT * FROM materials WHERE name = ? COLLATE NOCASE AND brand = ? COLLATE NOCASE LIMIT 1", (name, brand),).fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            raise RuntimeError(f"Error while getting the material: {e}") from e

    def exists_by_name(self, name, brand):
        return self.get_by_name(name, brand) is not None



