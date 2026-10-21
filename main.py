from database.connection import initialize_database


def main():
    initialize_database()
    print("Nexora-ERP iniciado correctamente")


if __name__ == "__main__":
    main()