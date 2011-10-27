.. _soft_delete_models:

=====================
Soft deletable models
=====================

There is a lot of occassions when you want some record not permanently removed
when user click "Delete" but just made inactive. This can be for a lot 
of reasons (to keep history of old orders in e-shop etc.).

Soft deletable models package gives you Django model subclass implementing
this repeting task. This package is very simple and consist only of two
classes.

.. py:class:: SoftDeletableModel(models.Model)

    :py:class:`SoftDeletableModel` is an abstract Django model subclass.
    
    The :py:class:`SoftDeletableModel` suclasses receive one extra attribute,
    ``active`` that signals if the record has been deleted or not. It also
    defines default model manager class: :py:class:`SoftDeletableModelManager`. 
    If you need to use custom manager for your :py:class:`SoftDeletableModel`
    subclass, be sure that your manager subclasses :py:class:`SoftDeletableModelManager`
    too.
    
    When delete is called on subclass, nothing bad really happens, only 
    the ``active`` flag is updated to False.
    

.. py:class:: SoftDeletableModelManager(models.Manager)

    This is Django model manager subclass that filters out deleted records
    by default.
    
    If you want your deleted records in your queryset, use :py:meth:`with_deleted`.
    
    .. py:method:: with_deleted(self)
    
        Adds deleted records to the queryset.
