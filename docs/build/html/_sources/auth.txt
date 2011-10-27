.. _auth:

======================================
Authentication/Authorization utilities
======================================


PermissionDeniedMiddleware
==========================

Django doesn't have build-in support for handling ``PermissionDenied`` exceptions.

Here is one.

To use it, optionally create ``403.html`` in your templates and add 
``fragapy.auth.middlware.PermissionDeniedMiddleware`` to your ``MIDDLEWARE_CLASSES``.


