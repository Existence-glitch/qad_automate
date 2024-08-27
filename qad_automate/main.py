import sys, time
from qad_ssh import get_ssh_session
from qad_login import login_qad
from qad_menus import select_menu

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <qad_version> <menu_number>")
        sys.exit(1)
    
    qad_version = sys.argv[1]
    #menu_number = sys.argv[2]
    
    try:
        session = get_ssh_session(qad_version)
        print("Session created")
        login_qad(session, qad_version)
        #select_menu(session, menu_number)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()
