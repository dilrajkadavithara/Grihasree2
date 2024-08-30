from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse

class Service(models.Model):
    service_id = models.CharField(max_length=20, primary_key=True)
    service_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.service_name
    
    def get_absolute_url(self):
        return reverse('api:service-detail', args=[str(self.service_id)])

class District(models.Model):
    district_id = models.CharField(max_length=20, primary_key=True)
    district_name = models.CharField(max_length=100, unique=True)
    state_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.district_name}"
    
    def get_absolute_url(self):
        return reverse('api:district-detail', args=[str(self.district_id)])

class LocalArea(models.Model):
    local_area_id = models.CharField(max_length=20, primary_key=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='local_areas')
    local_area_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.local_area_name}, {self.district.district_name}"
    
    def get_absolute_url(self):
        return reverse('api:local-area-detail', args=[str(self.local_area_id)])

class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    local_area = models.ForeignKey(LocalArea, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (f"Name: {self.name}, "
                f"Phone: {self.phone_number}, "
                f"Service: {self.service.service_name}, "
                f"District: {self.district.district_name}, "
                f"Local Area: {self.local_area.local_area_name}, "
                f"Created At: {self.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    def get_absolute_url(self):
        return reverse('api:lead-detail', args=[str(self.id)])
