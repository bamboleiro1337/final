import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:

    DATABASE_NAME = os.getenv('DATABASE_NAME', '')
    DATABASE_USER = os.getenv('DATABASE_USER', '')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_HOST = os.getenv('DATABASE_HOST', '')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '')

    TOKEN_SECRET=os.getenv('TOKEN_SECRET') or ''
    TOKEN_ALGORITHM=os.getenv('TOKEN_ALGORITHM') or ''

    MAX_NOTES_LEN = 200

    MIN_PASSWORD_LENGTH = 8

    @property
    def DATABASE_CONFIG(self):
        return f'postgresql+asyncpg://{Settings.DATABASE_USER}:{Settings.DATABASE_PASSWORD}@' \
               f'{Settings.DATABASE_HOST}:{Settings.DATABASE_PORT}/{Settings.DATABASE_NAME}'