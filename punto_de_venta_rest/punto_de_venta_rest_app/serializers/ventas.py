from rest_framework import serializers
from punto_de_venta_rest_app.models import Cliente

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'