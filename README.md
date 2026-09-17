# Salon Management System - Backend

This is the backend for the Salon Management System, built with Django and Django REST Framework (DRF).

## Features
- **Services API**: Endpoints to create, read, update, and delete salon services.
- **Appointments API**: Endpoints to book and manage appointments.
- **Validation**: Enforces business rules (positive prices/durations, required fields).

## Setup Instructions

0. **Add the virtual environment**:
   ```bash
   python -m venv .venv
   ```

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Seed Initial Data**:
   Populate the database with sample services.
   ```bash
   python manage.py seed_data
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://127.0.0.1:8000/api/`.

## API Endpoints

### Services
- `GET /api/services/` - List all services
- `POST /api/services/` - Create a new service
- `PUT /api/services/<id>/` - Update a service
- `DELETE /api/services/<id>/` - Delete a service

### Appointments
- `GET /api/appointments/` - List all appointments
- `POST /api/appointments/` - Create a new appointment
- `PATCH /api/appointments/<id>/status/` - Update an appointment status
- `DELETE /api/appointments/<id>/` - Delete an appointment
