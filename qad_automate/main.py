import sys
from qad_ssh import get_ssh_session
from qad_login import login_qad
from qad_menus import navigate_to_menu, list_menu_functions, execute_menu_function

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <qad_version> <menu_number>")
        sys.exit(1)

    qad_version = sys.argv[1]
    menu_number = sys.argv[2]

    try:
        session = get_ssh_session(qad_version)
        login_qad(session, qad_version)
        print(f"Successfully logged in to {qad_version}")

        navigate_to_menu(session, menu_number)
        
        available_functions = list_menu_functions(qad_version, menu_number)
        if available_functions:
            print(f"Available functions for menu {menu_number} in {qad_version} version:")
            for i, func in enumerate(available_functions, 1):
                print(f"{i}. {func}")
            
            choice = input("Enter the number of the function you want to execute (or 'q' to quit): ")
            if choice.lower() == 'q':
                print("Exiting...")
            elif choice.isdigit() and 1 <= int(choice) <= len(available_functions):
                function_name = available_functions[int(choice) - 1]
                execute_menu_function(session, qad_version, menu_number, function_name)
            else:
                print("Invalid choice. Exiting...")
        else:
            print(f"No functions available for menu {menu_number} in {qad_version} version")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()