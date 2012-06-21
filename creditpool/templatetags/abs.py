from django import template
from __builtin__ import abs as _abs

register = template.Library()

@register.filter()
def abs(value):
	return _abs(value)
