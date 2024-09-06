from utils import run_cmd, enter, space
from config import CONFIG

def login_qad(session, qad_version, domain_name):
    if qad_version in CONFIG:
        if qad_version.startswith('new'):
            login_qad_new(session, CONFIG[qad_version], domain_name)
        elif qad_version.startswith('old'):
            login_qad_old(session, CONFIG[qad_version], domain_name)
    else:
        print(f"Invalid QAD version: {qad_version}")

def login_qad_new(session, config, domain_name):
    s = session
    run_cmd(s, 'qadmenu' + enter(), wait_for = "~$")
    run_cmd(s, 'US' + enter())
    run_cmd(s, config['user'] + enter(), wait_for = "Enter data or press F4 to end.")
    run_cmd(s, config['pass'] + enter())
    run_cmd(s, domain_name + enter())
    run_cmd(s, space())

def login_qad_old(session, config, domain_name):
    s = session
    run_cmd(s, config['qadmenu'], debug=True)
    run_cmd(s, config['user'] + enter(), debug=True)
    run_cmd(s, config['pass'] + enter(), debug=True)
    run_cmd(s, domain_name + enter(), debug=True)
    run_cmd(s, space(), debug=True)