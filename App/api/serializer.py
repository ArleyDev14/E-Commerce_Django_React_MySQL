from rest_framework import serializers
from App.models import *

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model= Stock
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class DetailSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail_Sales
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Items
        fields = '__all__'