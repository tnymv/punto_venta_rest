from rest_framework import serializers
from punto_de_venta_rest_app.models import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'