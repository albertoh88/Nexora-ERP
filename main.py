import os
import time

from database.connection import initialize_database
from repositories.material_repository import MaterialRepository
from services.material_service import MaterialService

material_service = MaterialService()

# Colores
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
CYAN    = "\033[36m"
MAGENTA = "\033[35m"
WHITE   = "\033[37m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
RESET   = "\033[0m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"""
{CYAN}{BOLD}
 ███╗   ██╗███████╗██╗  ██╗ ██████╗ ██████╗  █████╗ 
 ████╗  ██║██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██╔══██╗
 ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║██████╔╝███████║
 ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║██╔══██╗██╔══██║
 ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝██║  ██║██║  ██║
 ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
{RESET}{DIM}          Sistema de Gestión de Costos & Materiales{RESET}
""")

def separator(char="═", length=50):
    print(f"{CYAN}{char * length}{RESET}")

def print_option(num, text, color=WHITE):
    print(f"  {BOLD}{CYAN}[{num}]{RESET}  {color}{text}{RESET}")

def invalid_option():
    print(f"\n  {RED}{BOLD}✖  Opción inválida{RESET}")
    time.sleep(0.8)

def pause():
    input(f"\n  {DIM}Presiona Enter para continuar...{RESET}")

# ===================== MATERIALES =====================
def menu_materials():
    while True:
        clear()
        banner()
        separator()
        print(f"  {BOLD}{YELLOW}MATERIALES{RESET}")
        separator()
        print()
        print_option("1", "Registro de materiales", GREEN)
        print_option("2", "Consultar materiales", BLUE)
        print_option("3", "Actualizar materiales", YELLOW)
        print_option("4", "Desactivar materiales", RED)
        print()
        print_option("0", "Volver al menú principal", DIM)
        print()
        separator()

        option = input(f"  {BOLD}Seleccione una opción › {RESET}").strip()

        if option == "1":
            clear()
            print(f"\n  {GREEN}{BOLD}→ Registro de materiales{RESET}")
            material_name = input(f"  {BOLD}Nombre del material {RESET}").strip()
            material_marca = input(f"  {BOLD}Marca del material {RESET}").strip()
            material_cantidad = int(input(f"  {BOLD}Cantidad de material {RESET}"))
            material_total_cost = int(input(f"  {BOLD}Total de costo {RESET}"))
            result = material_service.register_material(material_name, material_marca, material_cantidad, material_total_cost)
            if result:
                print("Registro con exito")
            else:
                print("No se pudo realizar el registro")
            pause()
        elif option == "2":
            clear()
            print(f"\n  {BLUE}{BOLD}→ Consultar materiales{RESET}")
            material_name = input(f"  {BOLD}Nombre del material {RESET}").strip()
            material_marca = input(f"  {BOLD}Marca del material {RESET}").strip()
            result = material_service.consult_material(material_name, material_marca)
            if result:
                print(result)
            else:
                print(result)
            pause()
        elif option == "3":
            clear()
            print(f"\n  {YELLOW}{BOLD}→ Actualizar materiales{RESET}")
            material_name = input(f"  {BOLD}Nombre del material {RESET}").strip()
            material_marca = input(f"  {BOLD}Marca del material {RESET}").strip()
            result = material_service.update_material(material_name, material_marca)
            pause()
        elif option == "4":
            clear()
            print(f"\n  {RED}{BOLD}→ Desactivar materiales{RESET}")
            pause()
        elif option == "0":
            break
        else:
            invalid_option()

# ===================== FICHAS DE COSTO =====================
def menu_cost_sheets():
    while True:
        clear()
        banner()
        separator()
        print(f"  {BOLD}{MAGENTA}FICHAS DE COSTO{RESET}")
        separator()
        print()
        print_option("1", "Crear ficha de costo", GREEN)
        print_option("2", "Consultar ficha de costo", BLUE)
        print_option("3", "Agregar material a una ficha", YELLOW)
        print_option("4", "Consultar componentes de una ficha", CYAN)
        print()
        print_option("0", "Volver al menú principal", DIM)
        print()
        separator()

        option = input(f"  {BOLD}Seleccione una opción › {RESET}").strip()

        if option == "1":
            clear()
            print(f"\n  {GREEN}{BOLD}→ Crear ficha de costo{RESET}")
            pause()
        elif option == "2":
            clear()
            print(f"\n  {BLUE}{BOLD}→ Consultar ficha de costo{RESET}")
            pause()
        elif option == "3":
            clear()
            print(f"\n  {YELLOW}{BOLD}→ Agregar material a una ficha{RESET}")
            pause()
        elif option == "4":
            clear()
            print(f"\n  {CYAN}{BOLD}→ Consultar componentes de una ficha{RESET}")
            pause()
        elif option == "0":
            break
        else:
            invalid_option()

# ===================== MENÚ PRINCIPAL =====================
def menu():
    while True:
        clear()
        banner()
        separator()
        print(f"  {BOLD}{WHITE}MENÚ PRINCIPAL{RESET}")
        separator()
        print()
        print_option("1", "Materiales", YELLOW)
        print_option("2", "Fichas de costo", MAGENTA)
        print()
        print_option("0", "Salir", RED)
        print()
        separator()

        option = input(f"  {BOLD}Seleccione una opción › {RESET}").strip()

        if option == "1":
            menu_materials()
        elif option == "2":
            menu_cost_sheets()
        elif option == "0":
            clear()
            print(f"\n  {CYAN}{BOLD}Hasta luego. Sistema NEXORA cerrado.{RESET}\n")
            time.sleep(0.7)
            break
        else:
            invalid_option()

def main():
    initialize_database()
    menu()



if __name__ == "__main__":
    main()