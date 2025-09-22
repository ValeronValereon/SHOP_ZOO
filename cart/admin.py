from django.contrib import admin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import datetime
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'address']
    readonly_fields = ['name', 'email', 'address', 'created_at']
    inlines = [OrderItemInline]
    actions = ['mark_as_delivered']

    @admin.action(description='Отметить как доставлено')
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'Обновлено {updated} заказов как "Доставлено".')

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Order.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                # Статус изменился — отправляем письмо
                html_message = render_to_string('cart/order_status_email.html', {
                    'order': obj,
                    'status': obj.get_status_display(),
                    'year': datetime.now().year
                })
                email = EmailMessage(
                    subject='Обновление статуса вашего заказа 🐾',
                    body=html_message,
                    from_email=None,
                    to=[obj.email]
                )
                email.content_subtype = 'html'
                email.send()
        super().save_model(request, obj, form, change)
