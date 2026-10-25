import os
import time
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from database.connection import initialize_database
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
    if os.name == "nt":
        os.system("cls")
    else:
        print("\033[2J\033[H", end="", flush=True)

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

def show_error(error):
    print(f"\n {RED}{BOLD}* {error}{RESET}")

# ===================== ENTRADA DE DATOS =====================

def ask_text(prompt, required=True):
    while True:
        value = input(f" {BOLD}{prompt} {RESET}").strip()
        if value or not required:
            return value
        print(f" {RED}Este campo não pode estar vazio{RESET}")

def ask_int(prompt, minimum=None):
    while True:
        raw = input(f" {BOLD}{prompt} {RESET}").strip()
        try:
            value = int(raw)
        except ValueError:
            print(f" {RED}Escreva um número inteiro{RESET}")
            continue
        if minimum is not None and value < minimum:
            print(f" {RED}Deve ser maior ou igual a {minimum}{RESET}")
            continue
        return value

def ask_money(prompt):
    """Peça um valor em reais (12,50 / 12,50 / R$ 1.234,56) e devolva-o em centavos."""
    while True:
        raw = input(f" {BOLD}{prompt} {RESET}").strip()
        raw = raw.upper().replace("R$", "").replace(" ", "")
        if "," in raw:
            raw = raw.replace(".", "").replace(",", ".")
        try:
            value = Decimal(raw)
        except InvalidOperation:
            print(f"  {RED}Escreva um valor válido, por exemplo 12.50{RESET}")
            continue
        if not value.is_finite() or value < 0:
            print(f"  {RED}O valor não pode ser negativo{RESET}")
            continue
        return int((value * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

# ===================== APRESENTAÇÃO =====================

def format_money(cents):
    """1234567 -> 'R$ 12.345,67'"""
    value = f"{Decimal(cents) / 100:,.2f}"
    value = value.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {value}"

def show_material(material):
    quantity = material["quantity"]
    total_cost = material["total_cost"]
    unit = material.get("unit", "un")
    unit_cost = (Decimal(total_cost) / 100 / quantity)
    unit_cost_text = f"R$ {unit_cost:.4f}".replace(".", ",")
    status = "Activo" if material["is_active"] else "Desactivado"

    print()
    print(f"  {BOLD}Nombre:{RESET}            {material['name']}")
    print(f"  {BOLD}Marca:{RESET}             {material['brand'] or '—'}")
    print(f"  {BOLD}Cantidad:{RESET}          {quantity} {unit}")
    print(f"  {BOLD}Costo total:{RESET}       {format_money(total_cost)}")
    print(f"  {BOLD}Costo por {unit}:{RESET}  {unit_cost_text}")
    print(f"  {BOLD}Estado:{RESET}            {status}")

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
            print(f"\n  {GREEN}{BOLD}→ Registro de materiales{RESET}\n")
            name = ask_text("Nombre del material")
            brand = ask_text("Marca del material (opcional)", required=False)
            quantity = ask_int("Cantidad de material", minimum=1)
            total_cost = ask_money("Costo total pagado (R$)")
            try:
                material_service.register_material(name, brand, quantity, total_cost)
                print(f"\n {GREEN}{BOLD}✔ Material registrado con éxito{RESET}")
            except (ValueError, RuntimeError) as e:
                show_error(e)
            pause()
        elif option == "2":
            clear()
            print(f"\n  {BLUE}{BOLD}→ Consultar materiales{RESET}\n")
            name = ask_text("Nombre del material")
            brand = ask_text(f"Marca del material (opcional)", required=False)
            try:
                material = material_service.consult_material(name, brand)
                if material is None:
                    print(f"\n  {RED}{BOLD}✖ No existe un material con ese nombre y marca{RESET}")
                else:
                    show_material(material)
            except (ValueError, RuntimeError) as e:
                show_error(e)
            pause()
        elif option == "3":
            clear()
            print(f"\n  {YELLOW}{BOLD}→ Actualizar materiales{RESET}\n")
            name = ask_text("Nombre del material")
            brand = ask_text(f"Marca del material (opcional)", required=False)
            try:
                current = material_service.consult_material(name, brand)
                if current is None:
                    print(f"\n  {RED}{BOLD}✖ No existe un material con ese nombre y marca{RESET}")
                else:
                    show_material(current)
                    print(f"\n  {DIM}Escribe los nuevos valores{RESET}\n")
                    quantity = ask_int("Cantidad de material", minimum=1)
                    total_cost = ask_money("Costo total pagado (R$)")
                    material_service.update_material(name, brand, quantity, total_cost)
                    print(f"\n  {GREEN}{BOLD}✔ Material actualizado con éxito{RESET}")
            except (ValueError, RuntimeError) as e:
                show_error(e)
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
    try:
        menu()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n  {CYAN}{BOLD}Sistema NEXORA cerrado.{RESET}\n")

if __name__ == "__main__":
    main()
