from django.urls import path
from .views import RegistrationAPIView, USStatesAPIView, AfricanCountriesAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('us-states/', USStatesAPIView.as_view(), name='us_states'),
    path('african-countries/', AfricanCountriesAPIView.as_view(), name='african_countries'),
]
