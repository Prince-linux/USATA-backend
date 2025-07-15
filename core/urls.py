from django.urls import path
from .views import RegistrationAPIView, USStatesAPIView, AfricanCountriesAPIView, ReutersAfricaFeed

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('us-states/', USStatesAPIView.as_view(), name='us_states'),
    path('african-countries/', AfricanCountriesAPIView.as_view(), name='african_countries'),
    path('rss/reuters-africa/', ReutersAfricaFeed.as_view()),

]
