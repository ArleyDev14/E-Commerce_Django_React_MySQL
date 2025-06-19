from django.core.mail import send_mail
from django.conf import settings

def send_payment_confirmation(user, order, payment):
    subject = f'Confirmación de pago - Orden #{order.id}'
    message = (
        f'Hola {user.first_name or user.username},\n\n'
        f'Tu pago ha sido registrado correctamente.\n\n'
        f'Orden: #{order.id}\n'
        f'Monto: ${payment.amount}\n'
        f'Método: {payment.payment_method}\n'
        f'Status del pago: {payment.status}\n\n'
        f'Gracias por tu compra.\n\n'
        f'Tu equipo de E-Commerce 🛒'
    )
    send_mail(
        subject,
        message,
        'no-reply@tu-ecommerce.com',
        [user.email],
        fail_silently=False
    )

def send_checkout_notification(user, order):
    subject = f'Confirmación de compra - Orden #{order.id}'
    message = (
        f'Hola {user.first_name or user.username},\n\n'
        f'Tu orden ha sido creada exitosamente y está pendiente de pago.\n\n'
        f'Orden: #{order.id}\n'
        f'Monto total: ${order.total_amount}\n'
        f'Status: {order.status}\n\n'
        f'¡Gracias por comprar con nosotros! 🛍️'
    )
    send_mail(
        subject,
        message,
        'no-reply@tu-ecommerce.com',
        [user.email],
        fail_silently=False
    )

def send_welcome_email(user):
    subject = '¡Bienvenido a nuestra tienda!'
    message = (
        f'Hola {user.first_name or user.username},\n\n'
        f'Te damos la bienvenida a nuestro e-commerce. 🎉\n\n'
        f'Desde hoy podrás explorar productos, realizar pedidos y más.\n\n'
        f'¡Gracias por unirte!\n\n'
        f'El equipo de la tienda 🛍️'
    )
    send_mail(
        subject,
        message,
        'no-reply@tu-ecommerce.com',
        [user.email],
        fail_silently=False
    )

def send_shipping_notification(user, order):
    subject = f'Tu orden #{order.id} ha sido enviada 🚚'
    message = (
        f'Hola {user.first_name or user.username},\n\n'
        f'Tu orden #{order.id} ha sido marcada como enviada.\n\n'
        f'Pronto la recibirás en tu dirección registrada.\n\n'
        f'Gracias por tu compra 🛍️'
    )
    send_mail(
        subject,
        message,
        'no-reply@tu-ecommerce.com',
        [user.email],
        fail_silently=False
    )