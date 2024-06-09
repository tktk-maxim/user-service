import os
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    if os.getenv('PYTEST_RUNNING') == 'true':
        return os.getenv('TEST_DATABASE_URL')
    return os.getenv('DATABASE_URL')


DATABASE_URL = get_database_url()

