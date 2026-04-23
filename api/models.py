from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# handle user registration and superuser creation
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password) # hash it
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# custom user model using email for login
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self): return self.email

# basic doctor info
class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    def __str__(self): return self.name

# patients are tied to the user who added them
class Patient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=15)
    
    def __str__(self): return self.name

# bridge table for patient-doctor assignments
class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('patient', 'doctor') # prevent double mapping
