from django.conf.urls.defaults import url, patterns
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from ella.core.custom_urls import resolver

from views import send_by_email

urlpatterns = patterns('',
    # send information about article to e-mail
    url(r'^%s/' % slugify(_('send by email')), send_by_email, name='send_email_new'),
)

resolver.register(urlpatterns)
