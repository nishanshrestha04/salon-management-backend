from django.core.management.base import BaseCommand
from appointments.models import Service, Appointment
from datetime import date, time

class Command(BaseCommand):
    help = "Seed initial salon services and sample appointments"

    def handle(self, *args, **kwargs):
        # 1. Seed Services
        services_data = [
            {"name": "Haircut", "price": 500.00, "duration": 30},
            {"name": "Hair Coloring", "price": 2500.00, "duration": 120},
            {"name": "Facial", "price": 1500.00, "duration": 60},
        ]

        services_dict = {}
        for item in services_data:
            service, created = Service.objects.get_or_create(
                name=item["name"],
                defaults={
                    "price": item["price"],
                    "duration": item["duration"],
                }
            )
            services_dict[service.name] = service
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created service: {service.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Service already exists: {service.name}"))

        # 2. Seed Sample Appointments
        appointments_data = [
            {
                "customer_name": "Ram Sharma",
                "customer_phone": "9841234567",
                "service": services_dict.get("Haircut"),
                "appointment_date": date(2026, 9, 18),
                "appointment_time": time(10, 0),
                "notes": "Regular haircut",
                "status": "pending",
            },
            {
                "customer_name": "Sita Thapa",
                "customer_phone": "9801234567",
                "service": services_dict.get("Facial"),
                "appointment_date": date(2026, 9, 18),
                "appointment_time": time(11, 0),
                "notes": "First visit",
                "status": "confirmed",
            },
        ]

        for apt in appointments_data:
            if not apt["service"]:
                continue
                
            appointment, created = Appointment.objects.get_or_create(
                customer_name=apt["customer_name"],
                appointment_date=apt["appointment_date"],
                appointment_time=apt["appointment_time"],
                service=apt["service"],
                defaults={
                    "customer_phone": apt["customer_phone"],
                    "notes": apt["notes"],
                    "status": apt["status"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created appointment for: {appointment.customer_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Appointment already exists for: {appointment.customer_name}"))

        self.stdout.write(self.style.SUCCESS("All seed operations completed successfully."))