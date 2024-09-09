from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LocalAreaSerializer, ServiceSerializer, DistrictSerializer, LeadSerializer
from gsapp.models import LocalArea, Service, District, Lead
from rest_framework import status
from django.db import OperationalError
from rest_framework.permissions import AllowAny
from django.views.generic import DetailView

import logging

logger = logging.getLogger(__name__)

# API Views (return JSON data for dropdowns and other dynamic elements)
class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class LocalAreaAPIListView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, district_id):
      try:
          local_areas = LocalArea.objects.filter(district_id=district_id)
          serializer = LocalAreaSerializer(local_areas, many=True)
          return Response(serializer.data)
      except (ConnectionError, OperationalError) as e:
          logger.error(f"Database error in LocalAreaAPIListView: {e}")
          return Response(
              {'error': 'A database error occurred. Please try again later.'},
              status=status.HTTP_503_SERVICE_UNAVAILABLE
          )
      except Exception as e:
          logger.exception(f"Unexpected error in LocalAreaAPIListView: {e}")
          return Response(
              {'error': 'An unexpected error occurred. Please try again later.'},
              status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )

  def options(self, request, *args, **kwargs):
      response = Response()
      response['Allow'] = 'GET, OPTIONS'
      response['Content-Type'] = 'application/json'
      return response

class ServiceAPIListView(APIView):
  permission_classes = [AllowAny]

  def get(self, request):
      try:
          services = Service.objects.all()
          serializer = ServiceSerializer(services, many=True)
          return Response(serializer.data)
      except Exception as e:
          logger.exception(f"Unexpected error in ServiceAPIListView: {e}")
          return Response(
              {'error': 'An unexpected error occurred. Please try again later.'},
              status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )

  def options(self, request, *args, **kwargs):
      response = Response()
      response['Allow'] = 'GET, OPTIONS'
      response['Content-Type'] = 'application/json'
      return response

class DistrictAPIListView(APIView):
  permission_classes = [AllowAny]

  def get(self, request):
      try:
          districts = District.objects.all()
          serializer = DistrictSerializer(districts, many=True)
          return Response(serializer.data)
      except Exception as e:
          logger.exception(f"Unexpected error in DistrictAPIListView: {e}")
          return Response(
              {'error': 'An unexpected error occurred. Please try again later.'},
              status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )

  def options(self, request, *args, **kwargs):
      response = Response()
      response['Allow'] = 'GET, OPTIONS'
      response['Content-Type'] = 'application/json'
      return response
  
class SubmitLeadView(APIView):
    def post(self, request):
        logger.debug("Received data:", request.data)
        serializer = LeadSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.debug("Data Received: ", request.data)
                logger.debug("Errors: ", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Failed to submit lead")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Detail Views (render HTML templates)
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'

class DistrictDetailView(DetailView):
    model = District
    template_name = 'district_detail.html'
    context_object_name = 'district'

class LocalAreaDetailView(DetailView):
    model = LocalArea
    template_name = 'local_area_detail.html'
    context_object_name = 'local_area'

class LeadDetailView(DetailView):
    model = Lead
    template_name = 'lead_detail.html'
    context_object_name = 'lead'

