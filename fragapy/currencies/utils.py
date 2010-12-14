from django.utils.numberformat import format

def format_price(price, currency):
    formatted_price = format(
        price,
        currency.decimal_separator,
        currency.decimal_places,
        thousand_sep=currency.thousand_separator
    )
    if currency.symbol_preceeds:
        params = (currency.symbol, formatted_price)
    else:
        params = (formatted_price, currency.symbol)
    return u'%s %s' % params
