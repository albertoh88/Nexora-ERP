# Ejecuta el SQL correspondiente

import sqlite3

from contextlib import closing
from database import connection

class MaterialRepository:

    def __init__(self):
        pass

    def update_material(self, material_name, material_brand, material_quantity, material_total_cost):
        try:
            with closing(connection.get_connection()) as conn:
                conn.execute("""UPDATE materials SET quantity = ?, total_cost = ?, updated_at = CURRENT_TIMESTAMP WHERE name = ? AND brand = ?""", (material_quantity, material_total_cost, material_name, material_brand))

                conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Error while updating the material: {e}") from e


    def insert_material(self, material_name, material_brand, material_quantity, material_total_cost):
        try:
            with closing(connection.get_connection()) as conn:

                conn.execute("""INSERT INTO materials (name, brand, quantity, total_cost) VALUES (?, ?, ?, ?)""", (material_name, material_brand, material_quantity, material_total_cost))

                conn.commit()
                return True
        except sqlite3.Error as e:
            raise RuntimeError(f"Error while inserting the material: {e}") from e


    def exists_by_name(self, material_name, material_brand):

        try:

            with closing(connection.get_connection()) as conn:

                cursor = conn.execute("""SELECT 1 FROM materials WHERE name = ? AND brand IS ? LIMIT 1""", (material_name,material_brand))

                return cursor.fetchone() is not None

        except sqlite3.Error as e:
            raise RuntimeError(f"Error while querying the material: {e}") from e


