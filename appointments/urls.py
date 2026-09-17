from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.service_list_create, name='service-list-create'),
    path('services/<int:pk>/', views.service_detail, name='service-detail'),
]