.. _static_sitemaps:

===============
Static sitemaps
===============

Static sitemaps is small pluggable Django application that wraps around the
``django.contrib.sitemaps`` framework. It's basic purpose is to enable
serving of sitemap files through your webserver and not Django application itself.

This has reasonable performance advantages. 

This app also gives you **Django management command** which will generate
sitemap files along with sitemap index file to your ``MEDIA_URL`` base path.

Installation
==============

First, it is necessary to add the application to your ``INSTALLED_APPS`` as 
usual::

    INSTALLED_APPS = (
        ...
        'fragapy.static_sitemaps',
        ...
    )

Second, you need to add one URL that will serve the Sitemap index file (sitemap.xml).
It goes like this::

    urlpatterns = patterns('',
        url(r'^sitemap.xml', include('fragapy.static_sitemaps.urls')),
    )
    
This will ensure that /sitemap.xml will be handled by static_sitemaps view. This
step can be avoided if you serve your media files from the same domain as your 
Django aplication lives on. In that case, you already have /sitemap.xml available.

If that's not the case (e.g. you media files live on different domain than the
application itself, like a subdomain or so) you should have this URL set up
so that /sitemap.xml is still available.

Next step is some small configuration. Put these into your settings file. There
are several configuration variables available:

``STATICSITEMAPS_ROOT_SITEMAP``
    This needs to point to the sitemap info dict which is used in common sitemaps
    framework, e.g.::
    
        from iw.charts.sitemaps import sitemaps as charts_sitemaps
        from iw.iwapp.sitemaps import sitemaps as iwapp_sitemaps

        sitemaps = {}
        sitemaps.update(iwapp_sitemaps)
        sitemaps.update(charts_sitemaps)
        
    In this example, we want to point our ``STATICSITEMAPS_ROOT_SITEMAP`` to
    the ``sitemaps`` variable, e.g.::
    
        STATICSITEMAPS_ROOT_SITEMAP = 'iw.sitemaps.sitemaps'
        
    The infodict contents are supposed to be same as for common sitemaps framework.
    We simply use the same classes.

``STATICSITEMAPS_SITEMAP_DOMAIN``
    This variable needs to be set to the domain on which the sitemaps files
    will be held. If you serve your media files from ``http://media.web.com``,
    this should be set to this URL.

``STATICSITEMAPS_USE_GZIP``
    This defaults to ``True``. Keep this unchanged if you want your sitemap
    files to be gzipped which is definitely beneficial and it is allowed
    in docs on sitemaps.org.
    
``STATICSITEMAPS_FILENAME_TEMPLATE``
    There is usually no need to change this.
    
    
CRON job to generate sitemaps
=============================

To generate sitemap files, we recommend using CRON job. There is a management
command that will refresh the sitemap files, usage is very simple::

    django-admin.py refresh_sitemap
    
After it finishes, it also **pings google** so that it will know that sitemap
has been updated.
