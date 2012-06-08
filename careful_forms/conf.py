from django.conf import settings
from appconf.base import AppConf


class CarefulFormsAppConf(AppConf):
    ENABLED = settings.DEBUG
    EXCEPTION_ON_WARNING = False

    class Meta:
        prefix = "careful"
