.. _versioning:

===========
Versioning
===========

The ``fragapy.versioning`` is simple package with tools to provide versioning
to you Django applications.

Most of utils which follows depend on one simple configuration variable expected
in your Django settings file. Example follows::

    VERSION = (1, 0, 0)

``fragapy.versioning.context_processors.version``
   This is a Django context processor that will add ``VERSION`` variable in 
   your template context. It can be feasible when you need to show application
   version in your web page footer or so. Configuration is simple,
   just add `fragarpy.versioning.context_processors.version` to your
   `TEMPLATE_CONTEXT_PROCESSORS` tuple in Django settings.
   
``fragapy.versioning.utils.get_version``
  This function returns the version tuple (e.g. `(1, 0, 0)`).
  
``fragapy.versioning.format.format_version``
  Simple function that formats version tuple in human sensible way.
  
  Results might be ``1.0.0.`` or ``1.0`` depending on the lenght of version
  tuple given.
