from django.db import models
from punto_de_venta_rest_app.models import Producto, Proveedor
# Create your models here.

class OrdenCompra(models.Model):
    numero_orden = models.CharField(max_length=20, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    estado_orden = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada')
    ], default='pendiente')
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Orden {self.numero_orden}'

class OrdenCompraProducto(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad}'