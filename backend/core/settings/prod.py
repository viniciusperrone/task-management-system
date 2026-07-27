from .base import *

from dotenv import load_dotenv

load_dotenv()


DEBUG = False
ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ['CORS_ALLOWED_ORIGINS']
