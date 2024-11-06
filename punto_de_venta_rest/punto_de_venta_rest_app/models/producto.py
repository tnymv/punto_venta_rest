from django.db import models
from punto_de_venta_rest_app.models import Proveedor

class CategoriaProducto(models.Model):
    nombre_categoria = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_categoria


class Producto(models.Model):
    
    codigo_producto = models.CharField(max_length=50, unique=True)
    nombre_producto = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_inventario = models.PositiveIntegerField(default=0)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_producto