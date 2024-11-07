from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from punto_de_venta_rest_app.viewsets import (UserViewSet, 
                                            CategoriaProductoViewSet, 
                                            ProductoViewSet,
                                            ProveedorViewSet,
                                            ClienteViewSet,
                                            PedidoViewSet
                                            )

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categoria-producto', CategoriaProductoViewSet)
router.register(r'producto', ProductoViewSet)
router.register(r'proveedor', ProveedorViewSet)
router.register(r'cliente', ClienteViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
