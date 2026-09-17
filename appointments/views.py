from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import ProtectedError
from .models import Service, Appointment
from .serializers import ServiceSerializer, AppointmentSerializer

@api_view(['GET', 'POST'])
def service_list_create(request):
    if request.method == 'GET':
        services = Service.objects.all().order_by('id')
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def service_detail(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({"error": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                {"error": "Cannot delete this service because it has existing appointments associated with it."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['GET', 'POST'])
def appointment_list_create(request):
    if request.method == 'GET':
        appointments = Appointment.objects.select_related('service').all().order_by('id')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Conflict check: same service, date, and time
        service = serializer.validated_data['service']
        appointment_date = serializer.validated_data['appointment_date']
        appointment_time = serializer.validated_data['appointment_time']

        conflict_exists = Appointment.objects.filter(
            service=service,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists()

        if conflict_exists:
            return Response(
                {"error": "This service is already booked for the selected date and time."},
                status=status.HTTP_409_CONFLICT
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'DELETE'])
def appointment_detail(request, pk):
    try:
        appointment = Appointment.objects.select_related('service').get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        new_status = request.data.get('status')
        valid_statuses = [choice[0] for choice in Appointment.STATUS_CHOICES]

        if not new_status or new_status not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Allowed values: {', '.join(valid_statuses)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment.status = new_status
        appointment.save()
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)