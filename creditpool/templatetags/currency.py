# based on http://djangosnippets.org/snippets/2326/
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

register = template.Library()

@register.filter(needs_autoescape=True)
def currency(value, grouping=True, autoescape=None):
	"""
	e.g.
	import locale
	locale.setlocale(locale.LC_ALL, 'de_CH.UTF-8')
	currency(123456.789)  # Fr. 123'456.79
	currency(-123456.789) # <span class="negative">Fr. -123'456.79</span>
	"""
	result = locale.currency(value, grouping=grouping)

	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x

	# add css class if value is negative
	if value < 0:
		# replace the minus symbol if needed
		if result[-1] == '-':
			length = len(locale.nl_langinfo(locale.CRNCYSTR))
			result = '%s-%s' % (result[0:length], result[length:-1])
		return mark_safe('<span class="negative">%s</span>' % esc(result))

	return result
