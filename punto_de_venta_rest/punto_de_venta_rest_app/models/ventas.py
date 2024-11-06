from django.db import models
from punto_de_venta_rest_app.models import Producto
# Create your models here.
class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_completo

class Pedido(models.Model):
    numero_pedido = models.CharField(max_length=20, unique=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estado_pedido = models.CharField(
    max_length=50, 
    choices=[
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado')
    ],
    default='pendiente'
)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Pedido {self.numero_pedido}'
    
    def calcular_precio_total(self):
        self.precio_total = sum(item.precio * item.cantidad for item in self.pedidoproducto_set.all())
        self.save()



class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre_producto}'