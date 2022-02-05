from google.cloud import storage
from google.oauth2 import service_account

from pathlib import Path

credentials = service_account.Credentials.from_service_account_file(Path(__file__).parent / './violet-harassment-e63f719390aa.json')