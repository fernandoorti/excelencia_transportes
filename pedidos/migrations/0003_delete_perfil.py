# Generated by Django 5.1 on 2024-09-20 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_telefono_remove_pedido_fecha_pedido_pedido_cancelado_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Perfil',
        ),
    ]
