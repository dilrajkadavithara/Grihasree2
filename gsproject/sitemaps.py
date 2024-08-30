from django.contrib.sitemaps import Sitemap
from gsapp.models import Service, District, LocalArea, Lead

class ServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Service.objects.all()

class DistrictSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return District.objects.all()

class LocalAreaSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return LocalArea.objects.all()

class LeadSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Lead.objects.all().order_by('created_at')  # Order by a relevant field, like created_at

    def lastmod(self, obj):
        return obj.created_at