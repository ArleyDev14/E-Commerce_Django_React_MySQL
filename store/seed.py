import random
from django.contrib.auth import get_user_model
from store.models import (
    Category, Product, ProductVariant, ProductImage,
    Cart, CartItem, Address, Order, OrderItem, Payment
)
from rest_framework.authtoken.models import Token

User = get_user_model()

print("🔥 Limpiando datos...")
CartItem.objects.all().delete()
Cart.objects.all().delete()
OrderItem.objects.all().delete()
Order.objects.all().delete()
Payment.objects.all().delete()
Address.objects.all().delete()
ProductImage.objects.all().delete()
ProductVariant.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()
User.objects.exclude(is_superuser=True).delete()

print("📦 Creando categorías...")
categories = []
for name in ['Ropa', 'Zapatos', 'Tecnología', 'Accesorios', 'Hogar']:
    cat = Category.objects.create(name=name, slug=name.lower())
    categories.append(cat)

print("👤 Creando usuarios...")
cliente = User.objects.create_user(username='cliente1', password='cliente123', email='cliente@example.com')
staff = User.objects.create_user(username='admin1', password='admin123', email='admin@example.com', is_staff=True)
Token.objects.get_or_create(user=cliente)
Token.objects.get_or_create(user=staff)

print("🧳 Creando productos, variantes e imágenes...")
productos = []
for i in range(10):
    p = Product.objects.create(
        title=f"Producto {i+1}",
        slug=f"producto-{i+1}",
        description="Este es un producto de prueba.",
        price=random.randint(10, 100),
        stock_quantity=100,
        is_active=True
    )
    p.categories.add(random.choice(categories))
    productos.append(p)

    for v in range(2):
        ProductVariant.objects.create(
            product=p,
            sku=f"SKU-{i+1}-{v+1}",
            size=random.choice(['S', 'M', 'L']),
            color=random.choice(['Rojo', 'Azul', 'Negro']),
            stock_quantity=50
        )

    ProductImage.objects.create(
        product=p,
        url="https://via.placeholder.com/300",
        alt_text="Imagen de producto",
        is_main=True
    )

print("📬 Creando dirección...")
address = Address.objects.create(
    user=cliente,
    line1="Calle Falsa 123",
    city="Bogotá",
    state="Cundinamarca",
    country="Colombia",
    postal_code="110111",
    is_default=True
)

print("🛒 Creando carrito con ítems...")
cart = Cart.objects.create(user=cliente)
variant = ProductVariant.objects.first()

if variant:
    CartItem.objects.create(cart=cart, product_variant=variant, quantity=2)

    print("📦 Generando orden con ítems...")
    order = Order.objects.create(
        user=cliente,
        address=address,
        status='pending',
        payment_status='pending',
        total_amount=variant.product.price * 2
    )

    OrderItem.objects.create(
        order=order,
        product_variant=variant,
        quantity=2,
        unit_price=variant.product.price
    )

    print("💳 Simulando pago...")
    Payment.objects.create(
        order=order,
        payment_method='card',
        transaction_id='TX123456789',
        amount=order.total_amount,
        status='success',
    )
else:
    print("⚠️ No se encontró ninguna variante. Verifica el modelo.")

print("✅ Seed completado exitosamente.")