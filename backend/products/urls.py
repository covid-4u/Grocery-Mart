from django.urls import path,include
from .views import ProductViewSet,CategoryViewSet,ProductsByCategoryView,CartViewSet,OrderViewSet,OrderItemViewSet,current_user
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet,basename='product')
router.register(r'category', CategoryViewSet)
router.register(r'cart', CartViewSet)
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')


urlpatterns = [
    path('', include(router.urls)),
    path('products/category/<str:category_name>/', ProductsByCategoryView.as_view(), name='products-by-category'),
    path('cart/get/', CartViewSet.as_view({'get': 'get_cart'}), name='get-cart'),
    path('current-user/', current_user, name='current_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

