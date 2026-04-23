from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import UserSerializer, PatientSerializer, DoctorSerializer, MappingSerializer

User = get_user_model()

# open signup endpoint
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# CRUD for patients
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # only show patients added by the current user
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # tie the patient to the current user
        serializer.save(user=self.request.user)

# simple CRUD for doctors
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

# handle assigning doctors to patients
class MappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # optional filtering by patient
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            return self.queryset.filter(patient_id=patient_id)
        return self.queryset
