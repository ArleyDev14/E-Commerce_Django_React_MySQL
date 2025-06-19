from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework import viewsets, filters
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsStaffOrReadOnly, IsStaffOnly, IsOwnerOrStaff
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .utils import send_payment_confirmation, send_checkout_notification, send_welcome_email, send_shipping_notification
from .filters import *
import decimal

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Address.objects.all()
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'categories']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'title']
    filterset_class = ProductFilter

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVarSerializer
    permission_classes = [IsStaffOrReadOnly]

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImgSerializer
    permission_classes = [IsStaffOnly]

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCatSerializer
    permission_classes = [IsStaffOnly]

class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsStaffOrReadOnly]
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Cart.objects.all()
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def checkout(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)

        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=400)

        address_id = request.data.get('address_id')
        if not address_id:
            return Response({'error': 'address_id is required'}, status=400)

        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return Response({'error': 'Invalid address'}, status=400)

        total = 0
        order = Order.objects.create(
            user=user,
            address=address,
            total_amount=0,
            status='pending',
            payment_status='pending'
        )

        for item in cart.items.all():
            price = item.product_variant.price_override or item.product_variant.product.price

            # Validación de stock
            if item.quantity > item.product_variant.stock_quantity:
                return Response({
                    'error': f"No hay suficiente stock para '{item.product_variant.product.title}'"
                }, status=400)

            total += price * item.quantity

            OrderItem.objects.create(
                order=order,
                product_variant=item.product_variant,
                quantity=item.quantity,
                unit_price=price
            )

            item.product_variant.stock_quantity -= item.quantity
            item.product_variant.save()

        order.total_amount = total
        order.save()
        cart.items.all().delete()
        send_checkout_notification(user, order)

        return Response({'message': 'Checkout completed', 'order_id': order.id})

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        # Solo staff puede ver todos. Usuario ve los suyos.
        if self.request.user.is_staff:
            return CartItem.objects.all()
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        # Busca el carrito del usuario autenticado y asocia automáticamente
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)

    def perform_update(self, serializer):
        # Asegura que no se intente cambiar el carrito por uno ajeno
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Staff ve todo, usuario solo lo suyo
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=self.request.user)
    
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsStaffOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all()
        return Review.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsStaffOnly]

class ProductDiscountViewSet(viewsets.ModelViewSet):
    queryset = ProductDiscount.objects.all()
    serializer_class = ProductDiscSerializer
    permission_classes = [IsStaffOnly]

############## REGISTERS ############################

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

            # ✉️ Notificación
            send_welcome_email(user)

            return Response({
                'message': 'User registered successfully',
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data

        # 1. Obtener orden
        try:
            order = Order.objects.get(id=data.get('order_id'), user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

        if order.payment_status == 'paid':
            return Response({'message': 'Order already paid'}, status=400)

        # 2. Validar monto
        try:
            sent_amount = decimal.Decimal(data.get('amount'))
        except:
            return Response({'error': 'Invalid amount'}, status=400)

        is_valid = sent_amount == order.total_amount

        # 3. Crear registro de pago (válido o fallido)
        payment = Payment.objects.create(
            order=order,
            payment_method=data.get('payment_method'),
            transaction_id=data.get('transaction_id'),
            amount=sent_amount,
            status='success' if is_valid else 'failed'
        )

        # 4. Actualizar orden solo si el pago es válido
        if is_valid:
            order.payment_status = 'paid'
            order.status = 'processing'
            order.save()
            send_payment_confirmation(request.user, order, payment)

        serializer = PaymentSerializer(payment)
        return Response({
            'message': 'Payment registered' if is_valid else 'Payment failed: incorrect amount',
            'payment': serializer.data
        }, status=201)

class MyOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
############## ADMIN ########################
class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class OrderAdminViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsStaffUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'payment_status']

    @action(detail=True, methods=['patch'], permission_classes=[IsStaffUser])
    def mark_as_shipped(self, request, pk=None):
        order = self.get_object()
        order.status = 'shipped'
        order.save()

        # Enviar notificación
        send_shipping_notification(order.user, order)

        return Response({'message': f'Orden #{order.id} marcada como enviada'})