from rest_framework import viewsets
from App.models import *
from App.api.serializer import *

class CategoriViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorieSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SaleSerializer

class DetailSaleViewSet(viewsets.ModelViewSet):
    queryset = Detail_Sales.objects.all()
    serializer_class = DetailSaleSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart_Items.objects.all()
    serializer_class = CartSerializer