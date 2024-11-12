from django.apps import AppConfig


class EmpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emp'

    def ready(self):
        # Import the Attendance and Performance models to ensure they are registered when the app is ready
        from .models import Attendance, Performance