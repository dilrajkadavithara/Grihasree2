from django.contrib import admin
from .models import Service, District, LocalArea, Lead

class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'phone_number', 'service', 'district', 'local_area', 'created_at')

class LocalAreaAdmin(admin.ModelAdmin):
    list_display = ('local_area_id','local_area_name', 'district')
    
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_id','district_name', 'state_name')
    
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id','service_name',)
    
admin.site.register(Lead,LeadAdmin)
admin.site.register(LocalArea, LocalAreaAdmin)  
admin.site.register(District, DistrictAdmin)
admin.site.register(Service, ServiceAdmin) 
