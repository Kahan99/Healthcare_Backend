from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, PatientViewSet, DoctorViewSet, MappingViewSet

# using router for clean REST urls
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'mappings', MappingViewSet, basename='mapping')

urlpatterns = [
    # auth
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # returns access + refresh
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # main api routes
    path('', include(router.urls)),
    
    # helper for patient doctors list
    path('mappings/patient/<int:patient_id>/', MappingViewSet.as_view({'get': 'list'}), name='patient_doctors'),
]
