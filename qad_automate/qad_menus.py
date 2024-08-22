from utils import send_command, execute_commands

# Gets menu number and selects the function that automatically enters that menu
def select_menu(session, menu_number):
    menu_parts = menu_number.split('.')
    for part in menu_parts:
        send_command(session, part + '\r')
    
    # After selecting the menu, call the corresponding function
    if menu_number in menu_logic:
        menu_logic[menu_number](session)
    else:
        print(f"No specific logic defined for menu {menu_number}")

# MENU CÓDIGOS GENERALIZADOS
def menu_36_2_13(session):
    commands = [
        'TEST SCRIPT PYTHON 1\r',
        'TEST SCRIPT PYTHON 1\r',
        '\r',
    ]

    execute_commands(session, commands)

# Map menu numbers to corresponding functions
menu_logic = {
    '36.2.13': menu_36_2_13,
    # Add other menus here
}