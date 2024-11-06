# views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from punto_de_venta_rest_app.models import Cliente
from punto_de_venta_rest_app.serializers import ClientesSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    """
    API para gestionar proveedor.

    - Búsqueda parcial:
        Usa el parámetro `?search=` para buscar coincidencias parciales en `nombre_proveedor` y `descripcion`.
        Ejemplo: `GET /api/proveedor/?search=Televisor`

    - Ordenamiento:
        Usa el parámetro `?ordering=` para ordenar por `nombre_empresa`.
        Usa `-` delante del campo para ordenar de forma descendente.
        Ejemplo ascendente: `GET /api/proveedor/?ordering=nombre_empresa`
        Ejemplo descendente: `GET /api/proveedor/?ordering=-nombre_empresa`
    """
    queryset = Cliente.objects.filter(activo = True)
    serializer_class = ClientesSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ["nombre_empresa"]
    search_fields = ["nombre_empresa"]
    ordering_fields = ["nombre_empresa"]