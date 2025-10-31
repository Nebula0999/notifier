import os
import json
import gspread
from typing import List

# Lazy client so we don't import Django settings at module import time and avoid
# circular imports between settings.py and this module.
_GSPREAD_CLIENT: gspread.client.Client | None = None

def _build_credentials_dict() -> dict:
  """
  Build a credentials dict from environment variables. Handles the common
  case where the private key is stored in an env var with escaped newlines.
  """
  private_key = os.getenv("PRIVATE_KEY")
  if private_key:
    # If the key was stored with literal '\n' sequences, convert them back
    # to real newlines which the google client expects.
    private_key = private_key.replace('\\n', '\n')

  creds = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": private_key,
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
  }
  # Remove keys that are None to avoid confusing the client
  return {k: v for k, v in creds.items() if v is not None}

def _get_gspread_client() -> gspread.client.Client:
  """
  Return a cached gspread client, creating it from environment credentials
  if necessary.
  """
  global _GSPREAD_CLIENT
  if _GSPREAD_CLIENT is None:
    creds = _build_credentials_dict()
    # gspread provides a helper that accepts a dict with service account
    # credentials.
    _GSPREAD_CLIENT = gspread.service_account_from_dict(creds)
  return _GSPREAD_CLIENT


def get_all_rows(doc_name: str, sheet_name: str = None, expected_headers: List[str] = None) -> List[dict]:
  """
  Fetches all rows from a given Google Sheet worksheet and returns a list
  of dictionaries using the first row as headers.
  
  Args:
    doc_name: Name of the Google Sheet document
    sheet_name: Name of the worksheet tab (optional, defaults to first sheet)
    expected_headers: List of expected column headers to handle duplicates (optional)
  """
  client = _get_gspread_client()
  sh = client.open(doc_name)
  if sheet_name:
    # Correct use of the worksheet accessor (it's a method, not subscriptable)
    worksheet = sh.worksheet(sheet_name)
  else:
    worksheet = sh.get_worksheet(0)
  
  # If expected headers provided, use them to handle duplicates
  if expected_headers:
    return worksheet.get_all_records(expected_headers=expected_headers)
  else:
    return worksheet.get_all_records()