====================
Django Careful Forms
====================

Django Careful Forms is a small extension on top of `django's Forms system`_. It
can help you discover potential security oversights in your forms.

It will emit warnings if there are any fields defined on forms that have not
been accessed (the asumption beeing that not accessed fields will also not have
been rendered in the template / displayed to the user).

.. _`django's Forms system`: https://docs.djangoproject.com/en/dev/topics/forms/

-------
Example
-------

Consider the following example:

.. code:: python

    # models.py:

    class SomeModel(models.Model):
        name = models.CharField(max_length=100)
        email = models.CharField(max_length=100)
        is_admin = models.BooleanField()


    class SomeForm(ModelForm):
        class Meta:
            model = SomeModel

    # template:

    {{ form.name }}
    {{ form.email }}


You might have noticed that the model form's ``Meta`` class misses an
``exclude`` definition for the is_admin field (assuming this is a form that is
going to be displayed to an end user).

Now on first glance this won't cause any problems since the template only
displays the name and email field. However by forgetting to exclude the
``is_admin`` field you are allowing users to change state internal to your
application (and in this hypothetical example gain admin rights).

If we changed this example to use careful-forms instead the missing field would
have triggerd a warning (or even an exception depending on settings, see below),
alerting you to the vulnerability.


----------
Motivation
----------

The initial motivation for this package came from the recently `well publicized
'mass assignment' vulnerability`_ in the Rails framework. The specifics are not
important but the basic problem was unchecked assignment of request data into a
model.

Of course django is not susceptible to this particular problem because of its
forms system. However even when using the forms system (especially when using
Model Forms) it is still possible to inadvertently allow request data to be
written to model fields that are supposed to be private (e.g. by forgetting to
exclude internal fields).

The final trigger however was Erik Romijn's nice talk `Building secure Django
websites`_ at djangocon europe 2012 which explicitly mentions the forms pitfall
in `slide 53ff.`_

.. _`well publicized 'mass assignment' vulnerability`: https://github.com/rails/rails/issues/5228
.. _`Building secure Django websites`: http://lanyrd.com/2012/djangocon-europe/srprk/
.. _`slide 53ff.`: https://speakerdeck.com/u/erik/p/building-secure-django-websites?slide=53

-------------
Compatibility
-------------

* Python 2.6+
* django 1.3+

------------
Installation
------------

The easy & recommended way:

    #~ `pip`_ install django-careful-forms

.. _`pip`: http://www.pip-installer.org/en/latest/index.html

-----
Usage
-----

#. Add ``"careful_forms.middleware.CarefulFormsMiddlware"`` to your projects
   ``settings.MIDDLEWARE_CLASSES``. You should add it near the beginning of the 
   list to make sure all forms are covered.

#. For every form that you want to be monitored by django-careful-forms change
   the base class of your forms to ``careful_forms.forms.CarefulModelForm`` (or
   ``CarefulForm`` for regular    forms) [1]_.

.. [1] In case you already have a custom form base class you can also add
   ``CarefulFormMixin`` to it.

Examples:

.. code:: python

    class MyForm(CarefulForm):
        # ...

    class OtherForm(CarefulModelForm):
        # ...

    class YetMoreForms(CarefulFormMixin, CustomFormBaseClass):
        # ...


--------
Settings
--------

CAREFUL_ENABLED
---------------

Default: ``settings.DEBUG``

This setting is the "main switch" for django-careful-forms. When set to ``True``
the recording of accessed form fields is active and `warnings`_ will be
triggered for not accessed fields. Since the bookkeping machinery incurs a
(small) per-request overhaed it is by default only enabled in ``DEBUG`` mode.

When set to ``False`` no pre-request runtime overhead is introduced.

.. _`warnings`: http://docs.python.org/library/warnings.html

CAREFUL_EXCEPTION_ON_WARNING
----------------------------

Default: ``False``

When set to ``True`` an exception is raised instead of a warning whenever a not
accessed field is detected.




