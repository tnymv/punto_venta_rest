from django.db import models
from punto_de_venta_rest_app.models import Producto, Pedido, OrdenCompra
# Create your models here.

class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    referencia_pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    referencia_orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.tipo_movimiento} de {self.cantidad} - {self.producto.nombre_producto}'

    @staticmethod
    def registrar_pedido(pedido):
        """
        Registra un movimiento de inventario para cada producto en el pedido cuando el pedido se completa.
        """
        if pedido.estado_pedido == 'completado':
            for item in pedido.pedidoproducto_set.all():
                # Registrar el movimiento de inventario
                MovimientoInventario.objects.create(
                    tipo_movimiento='salida',
                    producto=item.producto,
                    cantidad=item.cantidad,
                    referencia_pedido=pedido
                )
                # Ajustar el inventario del producto
                item.producto.cantidad_inventario -= item.cantidad
                item.producto.save()
