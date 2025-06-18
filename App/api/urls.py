from rest_framework.routers import DefaultRouter
from App.api.views import *

router = DefaultRouter()
router.register('categories',CategoriViewSet,basename='category')
router.register('products',ProductViewSet,basename='product')
router.register('stock',StockViewSet,basename='stock')
router.register('users',UserViewSet,basename='user')
router.register('sales',SaleViewSet,basename='sale')
router.register('detail_sales',DetailSaleViewSet,basename='detail_sale')
router.register('carts',CartViewSet,basename='cart')

urlpatterns = router.urls