from django.contrib import admin
from .models import Pedido, UnidadRT, Base, Telefono

admin.site.register(Pedido)
admin.site.register(UnidadRT)
admin.site.register(Base)
admin.site.register(Telefono)