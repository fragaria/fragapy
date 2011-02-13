from django.utils.formats import number_format
from decimal import Decimal, ROUND_HALF_UP

def format_price(price, currency, decimal_pos=0):

    d = Decimal(price)
    if decimal_pos == 0:
        exp = Decimal(1)
    else:
        exp = Decimal('1.0') / (Decimal(10) ** abs(decimal_pos))

    formatted_price = number_format(u'%s' % str(d.quantize(exp, ROUND_HALF_UP)), abs(decimal_pos))

    # formatted_price = number_format(price, decimal_pos)
    if currency.symbol_preceeds:
        params = (currency.symbol, formatted_price)
    else:
        params = (formatted_price, currency.symbol)
    return u'%s&nbsp;%s' % params
