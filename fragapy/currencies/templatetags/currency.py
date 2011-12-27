import types
from decimal import *

from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter

from fragapy.currencies.models import Currency
from fragapy.currencies.utils import format_price as fprc
from fragapy.currencies.utils import convert_price as cprc

from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def format_price(val, currency, decimal_pos):
	return fprc(val, currency, decimal_pos)

@register.filter
def price(val, args=None):
	if isinstance(args, types.StringTypes) and ',' in args:
		currency, decimal_pos = args.split(',', 1)
		decimal_pos = int(decimal_pos)
	else:
		currency = args
		decimal_pos = None
	if isinstance(currency, types.StringTypes):
		currency = Currency.objects.get(code=currency)
	try:
		float(val)
	except:
		return ''
	
	if currency is None:
		currency = Currency.objects.get_default()
	elif isinstance(currency, types.StringTypes):
		currency = Currency.objects.get(code=currency)
	
	if decimal_pos == "" or decimal_pos is None:
		decimal_pos = currency.decimal_places
	
	if not decimal_pos and val is not None and not float(val).is_integer():
		# if decimal places would hide some part of the price
		# and decimal pos is 0, set it to 2
		decimal_pos = 2
	
	if not isinstance(currency, Currency):
		return ''
	return mark_safe(fprc(val, currency, decimal_pos))
price.is_safe = True

@register.filter
def convert_price(price, currencies, curr_to=None):
	if curr_to is None:
		curr_orig, curr_target = currencies.split(",")
		curr_orig, curr_target = Currency.objects.get(code=curr_orig), Currency.objects.get(code=curr_target)
	else:
		curr_orig, curr_target = Currency.objects.get(code=currencies), Currency.objects.get(code=curr_to)
	
	return  cprc(price, curr_orig, curr_target)

@register.filter
def to_default_curr_using_factor(price, factor):
	c = Currency.objects.get_default()
	return mark_safe(fprc(price * factor, c, int(c.decimal_places)))
to_default_curr_using_factor.is_safe = True

def _calculate_price(price, currency):
	try:
		factor = Currency.objects.get(code__exact=currency).factor
	except Currency.DoesNotExist:
		if settings.DEBUG:
			raise Currency.DoesNotExist
		else:
			factor = Decimal('0.0')
	new_price = Decimal(price) * factor
	return new_price.quantize(Decimal('.01'), rounding=ROUND_UP)


@register.filter(name='currency')
@stringfilter
def set_currency(value, arg):
	return _calculate_price(value, arg)

class ChangeCurrencyNode(template.Node):
	def __init__(self, price, currency):
		self.price = template.Variable(price)
		self.currency = template.Variable(currency)

	def render(self, context):
		try:
			return _calculate_price(self.price.resolve(context),
				self.currency.resolve(context))
		except template.VariableDoesNotExist:
			return ''

@register.tag(name='change_currency')
def change_currency(parser, token):
	try:
		tag_name, current_price, new_currency = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError, '%r tag requires exactly two arguments' % token.contents.split()[0]
	return ChangeCurrencyNode(current_price, new_currency)
