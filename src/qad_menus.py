import importlib
from utils import run_cmd, enter

def get_menu_functions(qad_version, menu_number):
    try:
        module_name = f"menus.menu_{menu_number.replace('.', '_')}"
        menu_module = importlib.import_module(module_name)
        return menu_module.menu_functions
    except ImportError:
        print(f"No functions defined for menu {menu_number} in {qad_version} version")
        return {}

def navigate_to_menu(session, menu_number):
    run_cmd(session, menu_number + enter(), wait_for="blank to EXIT")
    print(f"Successfully navigated to menu {menu_number}")

def execute_menu_function(session, qad_version, menu_number, function_name):
    menu_functions = get_menu_functions(qad_version, menu_number)

    if function_name not in menu_functions:
        print(f"Function {function_name} not found for menu {menu_number} in {qad_version} version")
        return

    menu_functions[function_name](session)

def list_menu_functions(qad_version, menu_number):
    menu_functions = get_menu_functions(qad_version, menu_number)
    return list(menu_functions.keys())

