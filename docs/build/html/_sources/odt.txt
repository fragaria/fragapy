.. _odt:

=================================================
Printable output to ODT files (OpenOffice format)
=================================================

There are many times one wants to provide nice printable output to user while
trying to keep it as simple as possible to the programmer.

We have found one easy way to do this - **ODT templates** for OpenOffice!

These templates have strong advantage of being nothing else than **zipped XML file** which allows
use to work with them quite easily. In fact, you can do almost everything just
by opening them in OpenOffice or LibreOffice and edit them **like they were 
normal Django templates**.

Sometimes, you would want to do more complicated things and in those cases,
you will have to edit XML file directly but still, it's much more simple
than create directives to export the files as PDFs.

To make this even simpler, we have created some tools to work with ODT files.

Installation
============

Only thing you have to do is add ``fragapy.odt`` to your ``INSTALLED_APPS``
and set ``ODT_DIR`` to hold path where to look for your ODT files.


OdtPrintable class
===================

The easiest way to add print support to your model is to subclass :py:class:`OdtPrintable`. 
Just subclassing this method and creating one of following templates:

    * ``[app_label]/[object_name]/object_detail.odt``
    * ``[app_label]/object_detail.odt``
    * ``object_detail.odt``
    
does the trick and you can now have your view like this::

    def example_view(request, object_id):
        object = MyOdtPrintable.objects.get(pk=object_id)
        return object.print_to_response()
        
Which results in ODT being returned as response.

.. py:class:: OdtPrintable

    Allows for printing models as ODTs.
    
    .. py:method:: get_file_name(self)
    
        Returns file name of resulting ODT. Defaults to slugified ``unicode``
        called on ``self``.
        
    .. py:method:: get_template(self)
    
        Returns iterable of relative paths to look for template to render.
        
    .. py:method:: get_template_path(self)
    
        Returns full path to the first template returned by :py:meth:`get_template` or `None` if no template has been
        found.
        
    .. py:method:: get_context(self)
    
        Returns context that will be available in ODT template when rendering.
        
        Defaults to ``{'object': self}``
        
    .. py:method:: print_to_response(self, **kwargs)
    
        Returns ``HttpResponse`` containing the ODT file.
        
.. autofunction:: fragapy.odt.models.write_odt_to_stream
    
