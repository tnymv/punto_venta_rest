from django.apps import AppConfig

class PuntoDeVentaRestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'punto_de_venta_rest_app'

    def ready(self):
        import punto_de_venta_rest_app.signals