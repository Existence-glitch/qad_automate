import time, paramiko
from config import get_env_config
from utils import wait_for_string

def get_ssh_session(qad_version):
    try:
        ssh_config = get_env_config(qad_version)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=ssh_config['hostname'],
            username=ssh_config['username'],
            password=ssh_config['password']
        )

        session = ssh_client.get_transport().open_session()
        session.get_pty(term=ssh_config['termemul'])
        session.invoke_shell()

         # Wait for the login process to complete
        if not wait_for_string(session, "THIS SERVER HOSTS THE FOLLOWING QAD ENVIRONMENTS"):
            raise TimeoutError("Timed out waiting for the QAD environment to load")
        
        return session
    except KeyError as e:
        raise ValueError(f"Missing configuration key for {qad_version}: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to establish SSH connection for {qad_version}: {str(e)}")
