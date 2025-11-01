from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'daily'
    
    def items(self):
        return ['data-wall', 'users:login', 'users:signup']
    
    def location(self, item):
        return reverse(item)
