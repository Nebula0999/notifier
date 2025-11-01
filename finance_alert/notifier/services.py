import os
import json
import gspread
import time
from typing import List, Tuple, Optional

# Lazy client so we don't import Django settings at module import time and avoid
# circular imports between settings.py and this module.
_GSPREAD_CLIENT: Optional[gspread.client.Client] = None

# Simple in-process cache for sheet data to avoid expensive calls on every
# request (e.g., Render health checks). TTL can be tuned via env.
_CACHE: dict[Tuple[str, Optional[str], Tuple[str, ...]], tuple[float, list[dict]]] = {}
_CACHE_TTL_SECONDS = int(os.getenv("SHEETS_CACHE_TTL", "300"))  # default 5 minutes

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
    if not creds.get('private_key') or not creds.get('client_email'):
      raise RuntimeError(
        "Google Sheets credentials not configured. "
        "Set PRIVATE_KEY, CLIENT_EMAIL, and other env vars."
      )
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
  # Check cache first
  cache_key = (doc_name, sheet_name, tuple(expected_headers) if expected_headers else tuple())
  now = time.time()
  cached = _CACHE.get(cache_key)
  if cached and (now - cached[0]) < _CACHE_TTL_SECONDS:
    return cached[1]

  try:
    client = _get_gspread_client()
    sh = client.open(doc_name)
    if sheet_name:
      # Correct use of the worksheet accessor (it's a method, not subscriptable)
      worksheet = sh.worksheet(sheet_name)
    else:
      worksheet = sh.get_worksheet(0)

    # If expected headers provided, use them to handle duplicates
    rows = (
      worksheet.get_all_records(expected_headers=expected_headers)
      if expected_headers else
      worksheet.get_all_records()
    )
    # Update cache on success
    _CACHE[cache_key] = (now, rows)
    return rows
  except Exception:
    # On failure, serve stale cache if available; otherwise, return empty list
    if cached:
      return cached[1]
    return []