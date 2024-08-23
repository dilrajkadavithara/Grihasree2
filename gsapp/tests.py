from django.test import TestCase
from django.urls import reverse
from gsapp.models import Service, District, LocalArea
from django.contrib.auth.models import User

class FormSubmissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.service = Service.objects.create(service_id='S1', service_name='Plumbing')
        self.district = District.objects.create(district_id='D1', district_name='Ernakulam')
        self.local_area = LocalArea.objects.create(local_area_id='L1', local_area_name='Kochi', district=self.district)

    def test_valid_form_submission(self):
        """ Test valid form submission and check response status code. """
        response = self.client.post(reverse('api:submit-lead'), {
            'name': 'John Doe',
            'phone_number': '0123456789',  # Valid phone number
            'service': self.service.service_id,
            'district': self.district.district_id,
            'local_area': self.local_area.local_area_id
        })
        self.assertEqual(response.status_code, 201)  # API should return 201 CREATED

    def test_invalid_form_submission(self):
        """ Test invalid form submission returns proper error status. """
        response = self.client.post(reverse('api:submit-lead'), {
            'name': 'John Doe',
            'phone_number': '12345',  # Invalid phone number
            'service': self.service.service_id,
            'district': self.district.district_id,
            'local_area': self.local_area.local_area_id
        })
        self.assertEqual(response.status_code, 400)  # Expect 400 BAD REQUEST for invalid input

    def test_successful_form_submission(self):
        """ Test a successful form submission checks the response data. """
        response = self.client.post(reverse('api:submit-lead'), {
            'name': 'Jane Doe',
            'phone_number': '0123456789',
            'service': self.service.service_id,
            'district': self.district.district_id,
            'local_area': self.local_area.local_area_id
        })
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['name'], 'Jane Doe')
