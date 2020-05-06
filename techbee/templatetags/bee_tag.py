from django import template


register = template.Library()

@register.filter
def multiplie(value, args):
    return value * args

@register.filter
def hiki(value,args):
    return value - args
