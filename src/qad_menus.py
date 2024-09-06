import importlib
from utils import run_cmd, enter

def get_menu_functions(qad_version, menu_number):
    try:
        base_module_name = f"menus.menu_{menu_number.replace('.', '_')}"
        
        if qad_version.startswith('old'):
            module_name = f"{base_module_name}_old"
        else:
            module_name = base_module_name

        menu_module = importlib.import_module(module_name)
        return menu_module.menu_functions
    except ImportError:
        print(f"No functions defined for menu {menu_number} in {qad_version} version")
        return {}

def navigate_to_menu(session, qad_version, menu_number):
    wait_string = "" if qad_version.startswith('old') else "blank to EXIT"
    run_cmd(session, menu_number + enter(), wait_for=wait_string)
    print(f"Successfully navigated to menu {menu_number}")

def execute_menu_function(session, qad_version, menu_number, function_name, domain_name, function_index):
    menu_functions = get_menu_functions(qad_version, menu_number)

    if function_name not in menu_functions:
        print(f"Function {function_name} not found for menu {menu_number} in {qad_version} version")
        return

    menu_functions[function_name](session, domain_name, qad_version, menu_number, function_index)

def list_menu_functions(qad_version, menu_number):
    menu_functions = get_menu_functions(qad_version, menu_number)
    return list(menu_functions.keys())

