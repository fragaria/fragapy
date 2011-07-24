# odt templatetags
#
# line break <text:line-break/>
# paragraph <text:p></text:p>
#
# FIXME: DRAFT UNTESTED

from django import template


register = template.Library()

from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def odt_nl2br(text, *args):
    '''replaces \n\n with paragraph and \n with line break'''
    if text:
#        text = text.split("\n\n")
#        text = '<text:p>' + '<text:/p><text:p>'.join(text) + '</text:p>'
        text = text.replace("\n","<text:line-break/>")
    return mark_safe(text)

