# Validar e fazer cumprir as regras

from repositories.material_repository import MaterialRepository

class MaterialService:

    def __init__(self, repository=None):
        # Permite injetar um repositório falso nos testes
        self.repository = repository or MaterialRepository()

    # ---------- validação(uma vez, compartilhada) ----------

    @staticmethod
    def _clean_name(name):
        if not isinstance(name, str):
            raise ValueError("Material name must be text.")
        name = name.strip()
        if not name:
            raise ValueError("Material name cannot be empty.")
        return name

    @staticmethod
    def _clean_brand(brand):
        # A marca é opcional: é salvo "" em vez de Nenhum
        if brand is None:
            return ""
        if not isinstance(brand, str):
            raise ValueError("Material brand must be text.")
        return brand.strip()

    @staticmethod
    def _check_quantity(quantity):
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        return quantity

    @staticmethod
    def _check_total_cost(total_cost):
        if not isinstance(total_cost, int) or isinstance(total_cost, bool) or total_cost < 0:
            raise ValueError("Total cost must be a non-negative integer.")
        return total_cost

    def _clean_all(self, name, brand, quantity, total_cost):
        return self._clean_name(name), self._clean_brand(brand), self._check_quantity(quantity), self._check_total_cost(total_cost)

    # ---------- Casos de uso ----------

    def register_material(self, name, brand, quantity, total_cost):

        name, brand, quantity, total_cost = self._clean_all(name, brand, quantity, total_cost)

        if self.repository.exists_by_name(name, brand):
            raise ValueError("A material with this name and brand already exists.")
        return self.repository.insert_material(name, brand, quantity, total_cost)


    def update_material(self, name, brand, quantity, total_cost):

        name, brand, quantity, total_cost = self._clean_all(name, brand, quantity, total_cost)

        # Para atualizar, o material tem que existir

        if not self.repository.exists_by_name(name, brand):
            raise ValueError("Material not found.")
        return self.repository.update_material(name, brand, quantity, total_cost)


    def consult_material(self, name, brand=None):
        """Retorna os dados do material (dito) ou Nenhum se ele não existir."""
        name = self._clean_name(name)
        brand = self._clean_brand(brand)
        return self.repository.get_by_name(name, brand)

    def material_exists(self, name, brand=None):
        return self.consult_material(name, brand) is not None

    def deactivate_material(self, name, brand=None):
        return self._set_active(name, brand, 0)

    def reactivate_material(self, name, brand=None):
        return self._set_active(name, brand, 1)

    def _set_active(self, name, brand, is_active):
        name, brand = self._clean_name(name), self._clean_brand(brand)
        is_active = 0
        if not self.repository.exists_by_name(name, brand):
            raise ValueError("Material not found.")
        return self.repository.set_active(name, brand, is_active)



