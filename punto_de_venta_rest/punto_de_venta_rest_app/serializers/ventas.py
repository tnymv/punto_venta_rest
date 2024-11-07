from rest_framework import serializers
from punto_de_venta_rest_app.models import Cliente, Pedido, PedidoProducto, Producto

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ProductoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'codigo_producto', 'nombre_producto', 'descripcion', 'precio_venta']
        
class PedidoProductoSerializer(serializers.ModelSerializer):
    producto = ProductoDetailSerializer() 
    class Meta:
        model = PedidoProducto
        depth = 1 
        fields = ['producto', 'cantidad', 'precio']

class PedidoProductoReadSerializer(serializers.ModelSerializer):
    producto = ProductoDetailSerializer()

    class Meta:
        model = PedidoProducto
        fields = ['producto', 'cantidad', 'precio']
        
class PedidoParaCrearProductoSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = PedidoProducto
        fields = ['producto', 'cantidad', 'precio']
        
class PedidoSerializer(serializers.ModelSerializer):
    productos = PedidoParaCrearProductoSerializer(many=True, source='pedidoproducto_set', write_only=True)
    productos_detalle = PedidoProductoReadSerializer(many=True, source='pedidoproducto_set', read_only=True)

    class Meta:
        model = Pedido
        fields = ['numero_pedido', 'cliente', 'estado_pedido', 'precio_total', 'productos', 'productos_detalle']
        read_only_fields = ['precio_total']

    def create(self, validated_data):
        productos_data = validated_data.pop('pedidoproducto_set')
        pedido = Pedido.objects.create(precio_total=0.0, **validated_data)

        for producto_data in productos_data:
            producto = producto_data['producto']
            cantidad = producto_data['cantidad']
            precio = producto.precio_venta * cantidad
            PedidoProducto.objects.create(pedido=pedido, producto=producto, cantidad=cantidad, precio=precio)

        pedido.calcular_precio_total()
        return pedido
    
class PedidoConDetalleSerializer(serializers.ModelSerializer):
    productos = PedidoProductoSerializer(many=True, source='pedidoproducto_set')
    class Meta:
        model = Pedido
        depth = 1
        fields = fields = ['numero_pedido', 'cliente', 'estado_pedido', 'precio_total', 'productos']