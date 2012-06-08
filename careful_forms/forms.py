from django.forms.forms import Form
from django.forms.models import ModelForm
from logging import getLogger
from careful_forms.utils import AuditingSortedDict
from careful_forms.middleware import register_form
from careful_forms.conf import settings

log = getLogger(__name__)


#noinspection PySuperArguments
class CarefulFormMixin(object):
    """
    Form mixin class that keeps track of accessed fields
    """
    def __init__(self, *args, **kwargs):
        self.accessed_fields = set()
        self._fields = {}
        register_form(self)
        super(CarefulFormMixin, self).__init__(*args, **kwargs)

    def _record_field_access(self, field):
        self.accessed_fields.add(field)

    @property
    def not_accessed_fields(self):
        return set(self._fields.keys()) - self.accessed_fields

    @property
    def fields(self):
        return AuditingSortedDict(self._fields,
                                  on_key_access_callable=self._record_field_access)

    @fields.setter
    def fields(self, value):
        self._fields = value

    @fields.deleter
    def fields(self):
        self._fields = {}


if not settings.CAREFUL_ENABLED:
    # If we're disabled, replace the mixin with an empty one to avoid overhead
    class CarefulFormMixin(object):
        accessed_fields = set()
        not_accessed_fields = set()
        pass

    pass


class CarefulForm(CarefulFormMixin, Form):
    """
    Convenience `Careful` base class for regular django forms.
    For implementation see ``CarefulFormMixin``.
    """
    pass


class CarefulModelForm(CarefulFormMixin, ModelForm):
    """
    Convenience `Careful` base class for django model forms.
    For implementation see ``CarefulFormMixin``.
    """
    pass
