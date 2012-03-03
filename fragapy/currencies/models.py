from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

CURRENCY_CACHE = {}
DEFAULT_CURRENCY_CACHE = None

class CurrencyManager(models.Manager):
    use_for_related_fields = True

    def get(self, *args, **kwargs):
        global CURRENCY_CACHE
        key = ((key, val) for key, val in kwargs)
        if not key in CURRENCY_CACHE:
            CURRENCY_CACHE[key] = super(CurrencyManager, self).get(*args, **kwargs)
        return CURRENCY_CACHE[key]


    def get_default(self):
        global DEFAULT_CURRENCY_CACHE
        if DEFAULT_CURRENCY_CACHE is None:
            DEFAULT_CURRENCY_CACHE = self.get(is_default=True)
        return DEFAULT_CURRENCY_CACHE

class Currency(models.Model):
    code = models.CharField(_('code'), max_length=3)
    name = models.CharField(_('name'), max_length=25)
    symbol = models.CharField(_('symbol'), max_length=4)
    symbol_preceeds = models.BooleanField(_('symbol preceeds'), default=True,
        help_text=_('Is symbol placed before the price value?'))
    decimal_places = models.PositiveSmallIntegerField(_('decimal places'), default=2,
        help_text=_('How many decimal places should be used.'))
    decimal_separator = models.CharField(_('decimal separator'), max_length=1, default='.')
    thousand_separator = models.CharField(_('thousand separator'), max_length=2, default=' ')
    factor = models.DecimalField(_('factor'), max_digits=10, decimal_places=4,
        default=1, help_text=_('Difference between default currency and this one. '
        'Provide factor which represents ratio of this currency compared to the '
        'default currency. Eg. for CZK and EUR '
        '(assuming thath 1 EUR = 25 CZK): factor '
        'EUR when CZK is default = 0.04, factor CZK when EUR is be default = 1 / '
        '0.04 = 25.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('The currency will be available.'))
    is_default = models.BooleanField(_('default'), default=False,
        help_text=_('Make this the default currency.'))

    objects = CurrencyManager()

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __unicode__(self):
        return self.code

    def get_conversion_ratio(self, other_currency):
        """
        Returns conversion ratio for conversion from current currency to other currency.
        """
        return other_currency.factor / self.factor

    def save(self, **kwargs):
        if len(Currency.objects.filter(is_default=True)) == 0:
            self.is_default = True
        if self.is_default:
            self.factor = 1
            try:
                default_currency = Currency.objects.get(is_default=True)
            except Currency.DoesNotExist:
                pass
            else:
                default_currency.is_default = False
                default_currency.save()
            DEFAULT_CURRENCY_CACHE = self
        super(Currency, self).save(**kwargs)

    def get_quantize_constant(self):
        if self.decimal_places == 0:
            str = '1.'
        else:
            str = '.' + '1'.zfill(self.decimal_places)
        return Decimal(str)

