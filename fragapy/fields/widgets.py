from django.forms import Widget
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt

class DictionaryInputs(Widget):
    """
    A widget that displays dictionary key-value pairs
    as a list of text input box pairs

    Usage (in forms.py) :
    examplefield = forms.DictionaryField(label="Example Key Value Field",
        required=False, widget=DictionaryInputs(val_attrs={'size': 35},
        key_attrs={'class': 'large'}))
    """

    def __init__(self, *args, **kwargs):
        """
        A widget that displays Key Value inputs
        as a list of text input box pairs

        kwargs:
        key_attrs -- html attributes applied to the 1st input box pairs
        val_attrs -- html attributes applied to the 2nd input box pairs
        """
        self.key_attrs = {}
        self.val_attrs = {}
        self.key_labels = {}
        if "key_attrs" in kwargs:
            self.key_attrs = kwargs.pop("key_attrs")
        if "val_attrs" in kwargs:
            self.val_attrs = kwargs.pop("val_attrs")
        if "key_labels" in kwargs:
            self.key_labels = kwargs.pop("key_labels")

        Widget.__init__(self, *args, **kwargs)

    def render(self, name, value, attrs=None):
        """
        Renders this widget into an html string

        args:
        name  (str)  -- name of the field
        value (str)  -- dictionary automatically passed in by django
        attrs (dict) -- automatically passed in by django (unused in this function)
        """
        ret = ''
        if value and len(value) > 0:
            for k in sorted(value.keys()):
                v = value[k]
                ctx = {
                    'key': k,
                    'value': v,
                    'fieldname': name,
                    'key_attrs': flatatt(self.key_attrs),
                    'val_attrs': flatatt(self.val_attrs),
                    'label': self.key_labels[k] if self.key_labels.has_key(k) else k
                }
                ret += '<span>%(label)s:</span>&nbsp;<input type="hidden" name="key[%(fieldname)s]" value="%(key)s" %(key_attrs)s>&nbsp;<input type="text" name="value[%(fieldname)s]" value="%(value)s" %(val_attrs)s>&nbsp;' % ctx
        return mark_safe(ret)

    def value_from_datadict(self, data, files, name):
        """
        Returns the simplejson representation of the key-value pairs
        sent in the POST parameters

        args:
        data  (dict)  -- request.POST or request.GET parameters
        files (list)  -- request.FILES
        name  (str)   -- the name of the field associated with this widget

        """
        out = {}
        if data.has_key('key[%s]' % name) and data.has_key('value[%s]' % name):
            keys = data.getlist("key[%s]" % name)
            values = data.getlist("value[%s]" % name)
            for key, value in zip(keys, values):
                out[key] = value
        return out

