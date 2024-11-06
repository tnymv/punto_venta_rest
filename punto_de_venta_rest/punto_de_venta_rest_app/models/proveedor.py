from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=255)
    contacto_principal = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_empresa
