from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rest/v1/calendar/init/', views.GoogleCalendarInitView, name='init'),
    path('rest/v1/calendar/redirect/', views.GoogleCalendarRedirectView, name='callback'),
]