from app.utils.get_env import get_env

def mysql_config ():
    return {
        'host': get_env("DB_HOST", "mysql-example"),
        'user': get_env("DB_USER", "example_user"),
        'password': get_env("DB_PASSWORD", "example_password"),
        'database': get_env("DB_DATABASE", "example_db")
    }