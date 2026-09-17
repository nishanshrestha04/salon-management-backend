from rest_framework import serializers
from .models import Service, Appointment

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'duration', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Service name cannot be empty.")
        return value.strip()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be greater than zero minutes.")
        return value

class AppointmentSerializer(serializers.ModelSerializer):
    # PrimaryKeyRelatedField handles incoming foreign key IDs during POST
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    # Display the service name on read operations for the table
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'customer_name',
            'customer_phone',
            'service',
            'service_name',
            'appointment_date',
            'appointment_time',
            'notes',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def validate_customer_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Customer name cannot be empty.")
        return value.strip()

    def validate_customer_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Customer phone cannot be empty.")
        return value.strip()