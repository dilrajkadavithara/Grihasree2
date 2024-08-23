from rest_framework import serializers
from django.core.validators import RegexValidator
from gsapp.models import Lead,LocalArea,Service,District

class LeadSerializer(serializers.ModelSerializer):
    # If phone_number uses a custom validator, it can be declared like this
    phone_number = serializers.CharField(
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits.")]
    )
    # For foreign keys, you might use SlugRelatedField or PrimaryKeyRelatedField based on your form inputs
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    local_area = serializers.PrimaryKeyRelatedField(queryset=LocalArea.objects.all())

    class Meta:
        model = Lead
        fields = ['name', 'phone_number', 'service', 'district', 'local_area', 'created_at']

    def validate_name(self, value):
        # Validate that the name only contains letters and spaces
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError("Name must only contain letters and spaces.")
        return value

def validate_name(self, value):
        # Validate that the name only contains letters and spaces
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError("Name must only contain letters and spaces.")
        return value
      
class LocalAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalArea
        fields = ['local_area_id', 'local_area_name']  # Ensure these are the correct fields

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_id', 'service_name']  # Adjust these fields according to your model

# serializers.py

from rest_framework import serializers
from gsapp.models import District

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['district_id', 'district_name']  # Adjust these fields according to your model

