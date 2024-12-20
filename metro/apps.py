from django.apps import AppConfig

class MetroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metro'

    def ready(self):
        import metro.signals  # Import signals