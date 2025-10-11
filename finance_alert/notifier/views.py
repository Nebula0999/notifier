from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .services import get_all_rows
import requests
 
def data_wall(request):
  photos = get_all_rows("dataview")
  return render(request, 'data_wall.html', {'photos': photos})

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
