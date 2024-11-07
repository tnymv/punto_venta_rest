# views.py

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from punto_de_venta_rest_app.models import Cliente, Pedido
from punto_de_venta_rest_app.serializers import ClientesSerializer, PedidoSerializer, PedidoConDetalleSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """
    API para gestionar proveedor.

    - Búsqueda parcial:
        Usa el parámetro `?search=` para buscar coincidencias parciales en `nombre_proveedor` y `descripcion`.
        Ejemplo: `GET /api/proveedor/?search=Televisor`

    - Ordenamiento:
        Usa el parámetro `?ordering=` para ordenar por `nombre_completo`.
        Usa `-` delante del campo para ordenar de forma descendente.
        Ejemplo ascendente: `GET /api/proveedor/?ordering=nombre_completo`
        Ejemplo descendente: `GET /api/proveedor/?ordering=-nombre_completo`
    """
    queryset = Cliente.objects.filter(activo = True)
    serializer_class = ClientesSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ["nombre_completo"]
    search_fields = ["nombre_completo"]
    ordering_fields = ["nombre_completo"]


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
    @action(methods=["get"], detail=False)
    def get_pedidos_con_detalle(self, request, *args, **kwargs):
        pedidos_con_detalle = Pedido.objects.all()
        serializer_con_detalle = PedidoConDetalleSerializer(pedidos_con_detalle,many=True)
        data = {
            'count': len(serializer_con_detalle.data),
            'results': serializer_con_detalle.data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        """
        Endpoint para completar un pedido.
        """
        pedido = self.get_object()
        if pedido.estado_pedido != 'pendiente':
            return Response({'error': 'El pedido ya ha sido completado o cancelado.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        pedido.completar_pedido()
        serializer = self.get_serializer(pedido)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """
        Endpoint para cancelar un pedido.
        """
        pedido = self.get_object()
        if pedido.estado_pedido != 'pendiente':
            return Response({'error': 'El pedido ya ha sido completado o cancelado.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        pedido.cancelar_pedido()
        serializer = self.get_serializer(pedido)
        return Response(serializer.data)