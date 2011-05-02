from django.utils.formats import number_format
from decimal import Decimal, ROUND_HALF_UP

def format_price(price, currency, decimal_pos=None):
    if not currency:
        return price    

    if decimal_pos is None:
        decimal_pos = currency.decimal_places

    d = Decimal(str(price))
    if decimal_pos == 0:
        exp = Decimal(1)
    else:
        exp = Decimal('1.0') / (Decimal(10) ** abs(decimal_pos))

    formatted_price = number_format(u'%s' % str(d.quantize(exp, ROUND_HALF_UP)), abs(decimal_pos))
#    formatted_price = formatted_price.replace(' ', '&nbsp;')
    
    if currency.symbol_preceeds:
        params = (currency.symbol, formatted_price)
    else:
        params = (formatted_price, currency.symbol)
    return u'%s %s' % params
#    return u'%s&nbsp;%s' % params
