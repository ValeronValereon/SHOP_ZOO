from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return round(value * arg, 2)

@register.filter
def calc_total(items):
    return round(sum(item.quantity * item.price for item in items), 2)
