from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, Doctor, PatientDoctorMapping

User = get_user_model()

# handles signups
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}} # hide password in response

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['user'] # set automatically from request

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

# mapping with extra names for frontend convenience
class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'patient_name', 'doctor_name', 'assigned_date']
