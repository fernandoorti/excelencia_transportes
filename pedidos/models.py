from django.db import models
from datetime import time
from django.contrib.auth.models import User
from django.utils.timezone import now

# Definición de la clase Base
class Base(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, default='Dirección no especificada')

#
    def __str__(self):
        return self.nombre

# Definición de la clase UnidadRT
class UnidadRT(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='activo')
    nombre_operador = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Definición de la clase Telefono
class Telefono(models.Model):
    nombre = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

# Definición de la clase Pedido
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Asegúrate de que el ID 1 exista
    cliente = models.CharField(max_length=100)
    ubicacion_cliente = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    unidad_rt = models.ForeignKey(UnidadRT, null=True, blank=True, on_delete=models.SET_NULL)
  
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    fecha_hora_pedido = models.DateTimeField(default=now)
    telefono = models.ForeignKey(Telefono, on_delete=models.CASCADE)
    observacion = models.TextField(null=True, blank=True)
    cancelado = models.BooleanField(default=False)
    motivo_cancelacion = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.cliente} - {self.destino}"

# Definición del modelo UserProfile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255, default='Nombre por defecto')
    turno = models.CharField(max_length=50, blank=True, null=True)
    rango = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre_completo

# Opciones de turno y rango
TURNOS = [
    ('mañana', 'Mañana'),
    ('tarde', 'Tarde'),
    ('noche', 'Noche'),
]

RANGOS = [
    ('operador', 'Operador'),
    ('administrador', 'Administrador'),
]
