from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LocalAreaSerializer,ServiceSerializer,DistrictSerializer,LeadSerializer
from gsapp.models import LocalArea,Service,District,Lead
from rest_framework import status
from django.db import OperationalError


import logging

logger = logging.getLogger(__name__)



class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    
class LocalAreaListView(APIView):
    def get(self, request, district_id):
        try:
            # Filter local areas based on district_id
            local_areas = LocalArea.objects.filter(district_id=district_id)
            # Serialize data
            serializer = LocalAreaSerializer(local_areas, many=True)
            
            # Return serialized data
            return Response(serializer.data)

        except (ConnectionError, OperationalError) as e:
            # Handle database errors
            logger.error(f"Database error: {e}")
            return Response({'error': 'Database error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Catch-all for other unexpected errors
            logger.exception(f"Unexpected error: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
class DistrictListView(APIView):
    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)

class SubmitLeadView(APIView):
    def post(self, request):
        print("Received data:", request.data)
        serializer = LeadSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Data Received: ", request.data)
                print("Errors: ", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


