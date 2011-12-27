from django.utils import numberformat
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

    formatted_price = numberformat.format(
        u'%s' % str(d.quantize(exp, ROUND_HALF_UP)), currency.decimal_separator,
        abs(decimal_pos), grouping=3, thousand_sep=currency.thousand_separator)
    
    if currency.symbol_preceeds:
        params = (currency.symbol, formatted_price)
    else:
        params = (formatted_price, currency.symbol)
    return u'%s %s' % params


def convert_price(amount, curr_from, curr_to):
    return amount / curr_from.factor * curr_to.factor