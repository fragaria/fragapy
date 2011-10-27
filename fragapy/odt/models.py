'''
Created on 24.7.2011

@author: xaralis
'''
import os, zipfile, StringIO

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template.context import Context
from django.template import Template
from django.utils import encoding

try:
    ODT_DIR = getattr(settings, 'ODT_DIR')
except AttributeError:
    raise ImproperlyConfigured('Missing ODT_DIR atribute')

def write_odt_to_stream(stream, template_path, context={}):
    """
    Takes ODT template on given path, fills it with context and writes
    the result to stream.
    
    :param stream: Stream-like object to write to
    :param template_path: Full path to ODT template
    :param context: Context that will be passed to template when rendering
    """
    c = Context()
    for key, value in context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    # default mimetype
    mimetype = 'application/vnd.oasis.opendocument.text'
    # ODF is just a zipfile
    input = zipfile.ZipFile(template_path, "r")
    output = zipfile.ZipFile(stream, "a")
    # go through the files in source
    for zi in input.filelist:
        out = input.read(zi.filename)
        # wait for the only interesting file
        if zi.filename == 'content.xml':
            # un-escape the quotes (in filters etc.)
            t = Template(out.replace('&quot;', '"'))
            # render the document
            out = t.render(c)
        elif zi.filename == 'mimetype':
            # mimetype is stored within the ODF
            mimetype = out
        if type(out) != type('a'):
            out = encoding.smart_str(out, encoding='utf-8', strings_only=True,
                errors='strict')
        if out:
            output.writestr(zi.filename, out)
    output.close()
    return mimetype

class OdtPrintable(object):
    def get_file_name(self):
        """
        Returns resulting file name without .pdf extension
        """
        from django.template.defaultfilters import slugify
        return u'%s.odt' % slugify(unicode(self))

    def get_template(self):
        if (hasattr(self, '_meta')):
            app_label, object_name = self._meta.app_label, self._meta.object_name.lower()
            return (
                u'%s/%s/object_detail.odt' % (app_label, object_name),
                u'%s/object_detail.odt' % app_label,
                u'object_detail.odt'
            )
        return None

    def get_template_path(self):
        for template in self.get_template():
            full_path = os.path.join(ODT_DIR, template)
            if os.path.exists(full_path):
                return full_path
        return None

    def get_context(self):
        """
        Returns context for template
        """
        return {'object': self}

    def print_to_response(self, **kwargs):
        """
        Prints pdf content to the Django response object, which is returned
        """
        stream = StringIO.StringIO()
        mimetype = write_odt_to_stream(stream, self.get_template_path(), self.get_context())
        response = HttpResponse(content=stream.getvalue(), mimetype=mimetype)
        response['Content-Disposition'] = 'attachment; filename=%s' % self.get_file_name()
        return response

