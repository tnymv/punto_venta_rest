from rest_framework import serializers
from punto_de_venta_rest_app.models import CategoriaProducto, Producto, Proveedor

class CategoriaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProducto
        fields = ['id', 'nombre_categoria', 'descripcion']
        
        
class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=CategoriaProducto.objects.all())
    proveedor = serializers.PrimaryKeyRelatedField(queryset=Proveedor.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Producto
        depth = 1
        fields = [
            'id', 
            'codigo_producto', 
            'nombre_producto', 
            'descripcion', 
            'precio_venta', 
            'precio_compra', 
            'cantidad_inventario', 
            'proveedor', 
            'categoria', 
            'activo'
        ]