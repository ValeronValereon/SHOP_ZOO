from django.shortcuts import render, redirect, get_object_or_404
from shop_zoo.models import Product
from .models import CartItem, OrderItem
from .forms import OrderForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import datetime

# Получение ключа сессии пользователя
def get_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

# Отображение корзины
def view_cart(request):
    session_key = get_session_key(request)
    items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.get_total_price() for item in items)
    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total
    })

# Добавление товара в корзину
def add_to_cart(request, product_id):
    session_key = get_session_key(request)
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

# Очистка корзины
def clear_cart(request):
    session_key = get_session_key(request)
    CartItem.objects.filter(session_key=session_key).delete()
    return redirect('view_cart')

# Оформление заказа с HTML-письмом
def checkout(request):
    session_key = get_session_key(request)
    items = CartItem.objects.filter(session_key=session_key)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            total = sum(item.get_total_price() for item in items)

            # Генерация HTML-сообщения
            html_message = render_to_string('cart/order_email.html', {
                'order': order,
                'items': items,
                'total': total,
                'year': datetime.now().year
            })

            # Отправка письма
            email = EmailMessage(
                subject='Новый заказ 🐾',
                body=html_message,
                from_email=None,
                to=['barbosvaleron@gmail.com']
            )
            email.content_subtype = 'html'
            email.send()

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            items.delete()
            return render(request, 'cart/order_success.html', {'order': order})
    else:
        form = OrderForm()

    total = sum(item.get_total_price() for item in items)
    return render(request, 'cart/checkout.html', {
        'form': form,
        'items': items,
        'total': total
    })


