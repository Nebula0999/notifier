from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .services import get_all_rows
from .models import ReminderLog
import requests
 
def data_wall(request):
  """Display group contribution tracker from Google Sheets.
  
  Fetches daily contributions and running balances for Sultan, Blessing, 
  Cynthia, and Allan from the 'money mates tracker' Google Sheet.
  """
  # Define expected headers to handle duplicate column names
  expected_headers = [
    'Date', 'sultan', 'Blessing', 'cynthia', 'Allan',
    'challenge', 'sultan running', 'blessing running', 
    'cynthia running', 'Allan running'
  ]
  
  contributions = get_all_rows(
    "money mates tracker", 
    "daily log",
    expected_headers=expected_headers
  )
  
  # Calculate summary statistics for each member
  members = ['sultan', 'Blessing', 'cynthia', 'Allan']
  summary = {}
  
  for member in members:
    # Map member names to their running balance keys (case-sensitive)
    running_key_map = {
      'sultan': 'sultan running',
      'Blessing': 'blessing running',  # lowercase 'b' in sheet
      'cynthia': 'cynthia running',
      'Allan': 'Allan running'
    }
    running_key = running_key_map.get(member, f"{member} running")
    contrib_key = member
    
    # Get the latest running balance (last non-empty value)
    latest_balance = None
    total_contributed = 0
    days_contributed = 0
    
    for row in contributions:
      # Get running balance - handle both string and numeric values
      balance_val = row.get(running_key, '')
      if balance_val is not None and balance_val != '':
        balance_val = str(balance_val).strip()
        if balance_val:
          latest_balance = balance_val
      
      # Get contribution - handle both string and numeric values
      contrib_val = row.get(contrib_key, '')
      if contrib_val is not None and contrib_val != '':
        contrib_val = str(contrib_val).strip()
      if contrib_val and contrib_val not in ['-', '']:
        days_contributed += 1
        # Try to extract numeric value
        try:
          amount = float(contrib_val.replace('+', '').replace(',', ''))
          total_contributed += amount
        except ValueError:
          pass
    
    summary[member] = {
      'balance': latest_balance or '0',
      'total_contributed': total_contributed,
      'days_contributed': days_contributed
    }
  
  return render(request, 'data_wall.html', {
    'contributions': contributions,
    'summary': summary
  })

def proxy_image(request):
  """Simple image proxy view.

  Expects a query param `url` containing the image URL. This fetches the
  image server-side and streams it back to the client with the original
  Content-Type. This helps when external image URLs are protected or when
  the browser blocks loading them due to CORS or mixed-content issues.
  """
  url = request.GET.get('url')
  if not url:
    return HttpResponseBadRequest('Missing url param')

  try:
    resp = requests.get(url, stream=True, timeout=10)
  except requests.RequestException:
    return HttpResponse(status=502)

  if resp.status_code != 200:
    return HttpResponse(status=resp.status_code)

  content_type = resp.headers.get('Content-Type', 'application/octet-stream')
  response = HttpResponse(resp.raw, content_type=content_type)
  # Let the browser cache the image for a short period (adjust as needed)
  response['Cache-Control'] = 'public, max-age=600'
  return response


@login_required
def reminder_logs(request):
  """
  Display reminder send history.
  
  Shows only member names, timestamps, status, and balance - no email addresses
  for data protection.
  """
  logs = ReminderLog.objects.all().order_by('-sent_at')[:100]  # Last 100 logs
  
  # Group by member for quick stats
  member_stats = {}
  for log in ReminderLog.objects.all():
    if log.member_name not in member_stats:
      member_stats[log.member_name] = {'success': 0, 'failed': 0}
    member_stats[log.member_name][log.status] += 1
  
  return render(request, 'reminder_logs.html', {
    'logs': logs,
    'member_stats': member_stats
  })
