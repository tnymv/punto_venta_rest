# views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from punto_de_venta_rest_app.models import CategoriaProducto, Producto
from punto_de_venta_rest_app.serializers import CategoriaProductoSerializer, ProductoSerializer

class CategoriaProductoViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet para manejar el CRUD de Categorias de Producto.
    """
    queryset = CategoriaProducto.objects.all()
    serializer_class = CategoriaProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_categoria']

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar producto.

    Filtros disponibles:
    - Filtrado exacto:
        Puedes filtrar los producto por `categoria` y `proveedor` usando sus IDs.
        Ejemplo: `GET /api/producto/?categoria=1&proveedor=2`

    - Búsqueda parcial:
        Usa el parámetro `?search=` para buscar coincidencias parciales en `nombre_producto` y `descripcion`.
        Ejemplo: `GET /api/producto/?search=Televisor`

    - Ordenamiento:
        Usa el parámetro `?ordering=` para ordenar por `nombre_producto`, `precio_venta` o `cantidad_inventario`.
        Usa `-` delante del campo para ordenar de forma descendente.
        Ejemplo ascendente: `GET /api/producto/?ordering=precio_venta`
        Ejemplo descendente: `GET /api/producto/?ordering=-precio_venta`
    """
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("nombre_producto", "categoria", "proveedor")
    search_fields = ("nombre_producto", "descripcion")
    ordering_fields = ("nombre_producto", "precio_venta", "cantidad_inventario")

    def get_permissions(self):
        """
        Permite acceso de solo lectura sin autenticación, mientras que las operaciones de escritura requieren autenticación.
        """
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    
    def destroy(self, request, *args, **kwargs):
        """
        Permite eliminar la instancia que deseamos eliminar, como logica se uso un eliminado pasivo para 
        que el registro exista en bases de datos, pero que no pueda ser visto por el usuario
        - Resive como parametro la instancia o id que se quiere eliminar.
        - Retorna solamente un estado de `204` para identificar que no tiene contenido pero quie se realizo la acción de manera
        correcta
        """
        instance = self.get_object()
        instance.activo = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)