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

    def registrar_pedido(pedido):
        for item in pedido.pedidoproducto_set.all():
            MovimientoInventario.objects.create(
                tipo_movimiento='salida',
                producto=item.producto,
                cantidad=item.cantidad,
                referencia_pedido=pedido
            )
            item.producto.cantidad_inventario -= item.cantidad
            item.producto.save()
            
    def registrar_orden_compra(orden):
        """
        Registra los productos de una Orden de Compra en el inventario y actualiza la cantidad de inventario.

        Parameters:
        orden (OrdenCompra): La Orden de Compra a registrar en el inventario.

        Returns:
        None
        """
        for item in orden.ordencompraproducto_set.all():
            MovimientoInventario.objects.create(
                tipo_movimiento='entrada',
                producto=item.producto,
                cantidad=item.cantidad,
                referencia_orden_compra=orden
            )
            item.producto.cantidad_inventario += item.cantidad
            item.producto.save()
