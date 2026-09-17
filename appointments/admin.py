from django.contrib import admin
from .models import Service, Appointment

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'created_at')
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_phone', 'service', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'service')
    search_fields = ('customer_name', 'customer_phone')
