import sys
from qad_ssh import get_ssh_session
from qad_login import login_qad
from qad_menus import select_menu

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <menu_number>")
        sys.exit(1)
    
    # Gets menu to execute from the terminal
    menu_number = sys.argv[1]
    
    # Gets session, login and executes menu
    session = get_ssh_session()
    login_qad(session)
    select_menu(session, menu_number)
    
    # Close session after is finished
    session.close()

if __name__ == "__main__":
    main()
