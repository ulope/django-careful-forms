import sys
import warnings
from logging import getLogger
from django.core.exceptions import ImproperlyConfigured, MiddlewareNotUsed
from threading import local
from careful_forms.conf import settings

log = getLogger(__name__)

_secure_form_storage = local()


class SecurityWarning(RuntimeWarning):
    pass


def register_form(form):
    if hasattr(_secure_form_storage, "forms"):
        # Make sure middleware ran before trying to add anything
        frame = sys._getframe(2)
        _secure_form_storage.forms[id(form)] = {
            'form': form,
            'frame': {
                'file': frame.f_code.co_filename,
                'lineno': frame.f_lineno
            },
        }
    else:
        if (settings.CAREFUL_ENABLED and not
            'careful_forms.middleware.CarefulFormsMiddleware' in settings.MIDDLEWARE_CLASSES):
            # We're enabled and a form tried to register but the middleware
            # doesn't seem to be active - complain
            raise ImproperlyConfigured(
                "CarefulForms middleware appears to be missing. Please add it "
                "to your MIDDLEWARE_CLASSES setting."
            )

WARNING_MESSAGE = "The following fields on the form %r were probably not accessed: %s"
EXCEPTION_MESSAGE = ("The following fields on the form %r (instance created at "
                     "%s:%s) were probably not accessed: %s")


class CarefulFormsMiddleware(object):
    def __init__(self):
        if not settings.CAREFUL_ENABLED:
            raise MiddlewareNotUsed()

    def process_request(self, request):
        if settings.CAREFUL_ENABLED:
            _secure_form_storage.forms = {}

    def process_response(self, request, response):
        if settings.CAREFUL_ENABLED:
            if settings.CAREFUL_EXCEPTION_ON_WARNING:
                warnings.simplefilter("error", SecurityWarning)
            if len(_secure_form_storage.forms):
                for form_id, form_info in _secure_form_storage.forms.items():
                    not_accessed_fields = form_info['form'].not_accessed_fields
                    if settings.CAREFUL_EXCEPTION_ON_WARNING:
                        message = EXCEPTION_MESSAGE % (
                            form_info['form'],
                            form_info['frame']['file'],
                            form_info['frame']['lineno'],
                            ",\n".join(not_accessed_fields)
                        )
                    else:
                        message = WARNING_MESSAGE % (
                            form_info['form'],
                            ",\n".join(not_accessed_fields,)
                        )

                    if not_accessed_fields:
                        warnings.warn_explicit(
                            message,
                            SecurityWarning,
                            form_info['frame']['file'],
                            form_info['frame']['lineno']
                        )
                del _secure_form_storage.forms
        return response
