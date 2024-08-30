from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet,LocalAreaListView,sitemap_view,ServiceListView,DistrictListView,SubmitLeadView

app_name = 'api'

router = DefaultRouter()
router.register(r'leads', LeadViewSet,basename='lead')

urlpatterns = [
    path('', include(router.urls)),
    path('local-areas/<str:district_id>/', LocalAreaListView.as_view(), name='local-areas-list'),
    path('services/', ServiceListView.as_view(), name='services-list'),
    path('districts/', DistrictListView.as_view(), name='districts-list'),
    path('submit-lead/', SubmitLeadView.as_view(), name='submit-lead'),
]

