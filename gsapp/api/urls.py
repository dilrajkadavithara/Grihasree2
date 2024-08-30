from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, LocalAreaAPIListView, ServiceAPIListView, DistrictAPIListView, SubmitLeadView
from .views import ServiceDetailView, DistrictDetailView, LocalAreaDetailView

app_name = 'api'

router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')

urlpatterns = [
    # API Endpoints (return JSON data)
    path('', include(router.urls)),
    path('local-areas/<str:district_id>/', LocalAreaAPIListView.as_view(), name='local-areas-list'),
    path('services/', ServiceAPIListView.as_view(), name='services-list'),
    path('districts/', DistrictAPIListView.as_view(), name='districts-list'),
    path('submit-lead/', SubmitLeadView.as_view(), name='submit-lead'),

    # Template Rendering Endpoints (return HTML templates)
    path('service/<str:service_id>/', ServiceDetailView.as_view(), name='service-detail'),
    path('district/<str:district_id>/', DistrictDetailView.as_view(), name='district-detail'),
    path('local-area/<str:local_area_id>/', LocalAreaDetailView.as_view(), name='local-area-detail'),
]

