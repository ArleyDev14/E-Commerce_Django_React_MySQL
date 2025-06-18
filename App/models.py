from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=100, null=False)

class Products(models.Model):
    trade_name = models.CharField(max_length=255, null=False)
    trade_price = models.DecimalField(max_digits=5,decimal_places=2, null=False)
    discount_price = models.DecimalField(max_digits=5,decimal_places=2)
    categoria = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)

class Stock(models.Model):
    product_oid = models.ForeignKey(Products,on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField(null=False)

class Users(models.Model):
    ROLES = [
        ('ADMIN', 'ADMINISTRADOR'),
        ('USER', 'CLIENTE')
    ]
    email = models.EmailField(max_length=254, unique=True, null=True)
    username = models.CharField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    rol = models.CharField(max_length=100,choices=ROLES, default='USER')

class Sales(models.Model):
    STATES = [
        ('P', 'PENDING PAY'),
        ('S', 'SENT'),
        ('C', 'CANCELED'),
        ('R', 'RECEIVED')        
    ]
    user_oid = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    sale_date = models.DateField(auto_now_add=True,null=False)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    city = models.CharField(max_length=100,null=False)
    address = models.TextField(null=False)
    sale_state = models.CharField(max_length=100, null=False, choices=STATES)

class Detail_Sales(models.Model):
    sale_oid = models.ForeignKey(Sales, null=False, on_delete=models.CASCADE)
    product_oid = models.ForeignKey(Products,null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)

class Cart_Items(models.Model):
    user_oid = models.ForeignKey(Users, null=False, on_delete=models.CASCADE)
    Product_oid = models.ForeignKey(Products, null=False,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_at = models.DateField(auto_now=True)
