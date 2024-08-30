from django.contrib import admin
from django.urls import include, path
from gsapp.views import home,success
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ServiceSitemap, DistrictSitemap, LocalAreaSitemap, LeadSitemap

sitemaps = {
    'services': ServiceSitemap,
    'districts': DistrictSitemap,
    'local_areas': LocalAreaSitemap,
    'leads': LeadSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gsapp.api.urls', namespace='api')),  # Adjust the path according to your app structure
    path('', home, name='home'),  # Add this line to map the root URL to the home view
    path('success/', success, name='success'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
]

