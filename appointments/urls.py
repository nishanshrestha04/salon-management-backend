from django.urls import path
from . import views

urlpatterns = [
    # Servies URLS
    path('services/', views.service_list_create, name='service-list-create'),
    path('services/<int:pk>/', views.service_detail, name='service-detail'),

    # Appointments URLS
    path('appointments/', views.appointment_list_create, name='appointment-list-create'),
    path('appointments/<int:pk>/status/', views.appointment_detail, name='appointment-status-update'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment-detail'),
]