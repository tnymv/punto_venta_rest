# ventas/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido, PedidoProducto

@receiver(post_save, sender=Pedido)
def update_inventory_on_order(sender, instance, **kwargs):
    for item in instance.pedidoproducto_set.all():
        item.producto.cantidad_inventario -= item.cantidad
        item.producto.save()
