import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv('PYTEST_RUNNING') == 'true':
    DB_HOST = os.getenv('TEST_DB_HOST')
    DB_PORT = os.getenv('TEST_DB_PORT')
    DB_NAME = os.getenv('TEST_DB_NAME')
    DB_USER = os.getenv('TEST_DB_USER')
    DB_PASS = os.getenv('TEST_DB_PASS')
else:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')


DATABASE_CONFIG = {
    "connections": {"default": f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
