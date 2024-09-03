import sys
from qad_ssh import get_ssh_session
from qad_login import login_qad
from qad_menus import navigate_to_menu, list_menu_functions, execute_menu_function

def run_for_domain(qad_version, menu_number, function_index, domain_name):
    try:
        session = get_ssh_session(qad_version)
        login_qad(session, qad_version, domain_name)
        print(f"Successfully logged in to {qad_version} for domain {domain_name}")

        navigate_to_menu(session, menu_number)

        available_functions = list_menu_functions(qad_version, menu_number)
        if available_functions:
            if function_index is not None:
                if 0 <= function_index < len(available_functions):
                    function_name = available_functions[function_index]
                    print(f"Executing function: {function_name}")
                    execute_menu_function(session, qad_version, menu_number, function_name, domain_name)
                else:
                    print(f"Invalid function index. Available indices: 1 to {len(available_functions)}")
            else:
                print(f"Available functions for menu {menu_number} in {qad_version} version:")
                for i, func in enumerate(available_functions, 1):
                    print(f"{i}. {func}")

                choice = input("Enter the number of the function you want to execute (or 'q' to quit): ")
                if choice.lower() == 'q':
                    print("Exiting...")
                elif choice.isdigit() and 1 <= int(choice) <= len(available_functions):
                    function_name = available_functions[int(choice) - 1]
                    execute_menu_function(session, qad_version, menu_number, function_name, domain_name)
                else:
                    print("Invalid choice. Exiting...")
        else:
            print(f"No functions available for menu {menu_number} in {qad_version} version")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'session' in locals():
            session.close()
            print(f"QAD session for domain {domain_name} successfully closed")

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python main.py <qad_version> <menu_number> [function_index]")
        sys.exit(1)

    qad_version = sys.argv[1]
    menu_number = sys.argv[2]
    function_index = int(sys.argv[3]) - 1 if len(sys.argv) == 4 else None

    domains = ['SURFRUT', 'PUREFRUI']

    for domain in domains:
        print(f"\nExecuting for domain: {domain}")
        run_for_domain(qad_version, menu_number, function_index, domain)

if __name__ == "__main__":
    main()