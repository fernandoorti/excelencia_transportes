from django.apps import AppConfig

class PedidosConfig(AppConfig):  # Asegúrate de usar el nombre correcto de tu aplicación
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pedidos'  # El nombre de tu aplicación

    def ready(self):
        import pedidos.signals  # Asegúrate de que 'pedidos' sea el nombre correcto de tu aplicación
