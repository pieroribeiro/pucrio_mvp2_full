import os

def get_env(env_name: str, default_value: str):
    return os.getenv(env_name, default_value)