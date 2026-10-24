# Valida y aplica las reglas

from repositories.material_repository import MaterialRepository

class MaterialService:

    def __init__(self):
        self.material_repository = MaterialRepository()

    def update_material(self, material_name, material_brand, material_quantity, material_total_cost):
        if not isinstance(material_name, str):
            raise ValueError("Material name must be text.")

        material_name = material_name.strip()

        if not material_name:
            raise ValueError("Material name cannot be empty.")

        if material_brand is not None:
            material_brand = material_brand.strip() or None

        if (
                not isinstance(material_quantity, int)
                or isinstance(material_quantity, bool)
                or material_quantity <= 0
        ):
            raise ValueError("Quantity must be a positive integer.")

        if (
                not isinstance(material_total_cost, int)
                or isinstance(material_total_cost, bool)
                or material_total_cost < 0
        ):
            raise ValueError(
                "Total cost must be a non-negative integer."
            )

        if self.consult_material(material_name, material_brand):
            raise ValueError(
                "A material with this name and brand already exists."
            )

        return self.material_repository.update_material(material_name, material_brand, material_quantity, material_total_cost)

    def consult_material(self, material_name, material_brand=None):
        material_name = material_name.strip()

        if not material_name:
            return False

        if material_brand is not None:
            material_brand = material_brand.strip() or None

        return self.material_repository.exists_by_name(material_name, material_brand)

    def register_material(self, material_name, material_brand, material_quantity, material_total_cost):

        if not isinstance(material_name, str):
            raise ValueError("Material name must be text.")

        material_name = material_name.strip()

        if not material_name:
            raise ValueError("Material name cannot be empty.")

        if material_brand is not None:
            material_brand = material_brand.strip() or None

        if (
                not isinstance(material_quantity, int)
                or isinstance(material_quantity, bool)
                or material_quantity <= 0
        ):
            raise ValueError("Quantity must be a positive integer.")

        if (
                not isinstance(material_total_cost, int)
                or isinstance(material_total_cost, bool)
                or material_total_cost < 0
        ):
            raise ValueError(
                "Total cost must be a non-negative integer."
            )

        if self.consult_material(material_name, material_brand):
            raise ValueError(
                "A material with this name and brand already exists."
            )

        return self.material_repository.insert_material(
            material_name,
            material_brand,
            material_quantity,
            material_total_cost
        )


