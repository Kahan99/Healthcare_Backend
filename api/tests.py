from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class HealthcareAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')
        self.patient_url = reverse('patient-list')
        self.doctor_url = reverse('doctor-list')
        self.mapping_url = reverse('mapping-list')
        
        self.user_data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "password": "password123"
        }
        
    def test_registration_and_login(self):
        # 1. Register
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 2. Login
        login_data = {"email": self.user_data["email"], "password": self.user_data["password"]}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
        return response.data['access']

    def test_full_workflow(self):
        # Setup Auth
        token = self.test_registration_and_login()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        # 3. Add Patient
        patient_data = {"name": "Jane Doe", "age": 30, "gender": "Female", "contact": "9998887776"}
        response = self.client.post(self.patient_url, patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        patient_id = response.data['id']
        
        # 4. Add Doctor
        doctor_data = {
            "name": "Dr. House", 
            "specialization": "Diagnostics", 
            "phone": "5550199", 
            "email": "house@princeton.com"
        }
        response = self.client.post(self.doctor_url, doctor_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doctor_id = response.data['id']
        
        # 5. Create Mapping
        mapping_data = {"patient": patient_id, "doctor": doctor_id}
        response = self.client.post(self.mapping_url, mapping_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 6. List Mappings for Patient
        mapping_patient_url = reverse('patient_doctors', kwargs={'patient_id': patient_id})
        response = self.client.get(mapping_patient_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['doctor_name'], "Dr. House")

    def test_unauthenticated_access(self):
        # Try to get patients without token
        response = self.client.get(self.patient_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
