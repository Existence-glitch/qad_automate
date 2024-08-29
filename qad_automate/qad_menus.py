from utils import *


def navigate_to_menu_old(session, menu_number):
    """
    Navigate to the specified menu number.
    
    :param session: Paramiko session object
    :param menu_number: Menu number in the format "X.Y.Z"
    """
    menu_parts = menu_number.split('.')
    for part in menu_parts:
        run_cmd(session, part + enter())
    print(f"Successfully navigated to menu {menu_number}")

def navigate_to_menu(session, menu_number):
    """
    Navigate to the specified menu number.
    
    :param session: Paramiko session object
    :param menu_number: Menu number in the format "X.Y.Z"
    """
    run_cmd(session, menu_number + enter(), wait_for="blank to EXIT")
    print(f"Successfully navigated to menu {menu_number}")

def execute_menu_function(session, qad_version, menu_number, function_name):
    """
    Execute a specific function for the given menu number and QAD version.
    
    :param session: Paramiko session object
    :param qad_version: QAD version ('new' or 'old')
    :param menu_number: Menu number in the format "X.Y.Z"
    :param function_name: Name of the function to execute
    """
    menu_functions = menu_functions_new if qad_version.startswith('new') else menu_functions_old
    
    if menu_number not in menu_functions:
        print(f"No functions defined for menu {menu_number} in {qad_version} version")
        return
    
    if function_name not in menu_functions[menu_number]:
        print(f"Function {function_name} not found for menu {menu_number} in {qad_version} version")
        return
    
    menu_functions[menu_number][function_name](session)

def _36_2_13_test(s):
    run_cmd(s, "TEST Nombre de campo" + enter())
    run_cmd(s, "TEST Valor" + enter())
    run_cmd(s, "TEST Comentario" + enter())

def _61_3_16_getAll(s):
    run_cmd(s, enter_n(20))
    captured_output = capture_output(s, "archivo:", "-Para_Etiq_Bartender.csv", "cont_int.csv")
    print("El url capturado es: ", captured_output)
    run_cmd(s, space())
    
# Dictionary to store menu-specific functions for new QAD version
menu_functions_new = {
    "36.2.13": {
        "test": lambda session: _36_2_13_test(session),
    },
    "61.3.16": {
        "Extraer Todos": lambda session: _61_3_16_getAll(session),
    },
    # Add more menu numbers and their functions for new version as needed
}

# Dictionary to store menu-specific functions for old QAD version
menu_functions_old = {
    "36.2.13": {
        "test": lambda session: _36_2_13_test(session),
    },
    # Add more menu numbers and their functions for old version as needed
}

def list_menu_functions(qad_version, menu_number):
    """
    List available functions for the given menu number and QAD version.
    
    :param qad_version: QAD version ('new' or 'old')
    :param menu_number: Menu number in the format "X.Y.Z"
    :return: List of available function names
    """
    menu_functions = menu_functions_new if qad_version.startswith('new') else menu_functions_old
    
    if menu_number in menu_functions:
        return list(menu_functions[menu_number].keys())
    return []