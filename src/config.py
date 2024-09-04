import yaml
import os
from dotenv import load_dotenv

def load_config(config_filename='config.yaml'):
    # Load environment variables from .env file
    load_dotenv()

    # Get the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level to the parent directory of qad_automate
    parent_dir = os.path.dirname(current_dir)
    
    # Construct the path to the config folder
    config_folder = os.path.join(parent_dir, 'config')
    
    # Full path to the config file
    config_path = os.path.join(config_folder, config_filename)
    
    # Check if the config file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Replace environment variables for all environments
    for env, env_config in config.items():
        for key, value in env_config.items():
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                env_var = value[2:-1]
                env_value = os.getenv(env_var)
                if env_value is None:
                    raise ValueError(f"Environment variable {env_var} not set for {env}.{key}")
                config[env][key] = env_value
    
    return config

CONFIG = load_config()

def get_env_config(env):
    """
    Get the configuration for a specific environment.
    
    :param env: The environment key (e.g., 'new01', 'old02')
    :return: A dictionary with the environment's configuration
    """
    if env not in CONFIG:
        raise ValueError(f"Environment {env} not found in configuration")
    return CONFIG[env]

GOOGLESHEET_BASE_URL = "https://docs.google.com/spreadsheets/d/{}/edit"

def load_googlesheet_ids(config_filename='googlesheet_urls.yaml'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    config_folder = os.path.join(parent_dir, 'config')
    config_path = os.path.join(config_folder, config_filename)
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Google Sheet IDs config file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        ids_config = yaml.safe_load(file)
    
    return ids_config

GOOGLESHEET_IDS = load_googlesheet_ids()

def get_googlesheet_url(qad_version, menu_number, function_index):
    """
    Get the Google Sheet URL for a specific QAD version, menu number, and function index.
    
    :param qad_version: The QAD version (e.g., 'new02', 'new03')
    :param menu_number: The menu number (e.g., '61.3.16')
    :param function_index: The function index (e.g., 1)
    :return: The full Google Sheet URL or None if not found
    """
    try:
        spreadsheet_id = GOOGLESHEET_IDS[qad_version][menu_number][function_index]
        return GOOGLESHEET_BASE_URL.format(spreadsheet_id)
    except KeyError:
        return None