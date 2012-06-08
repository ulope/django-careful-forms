from logging import getLogger
from django.utils.datastructures import SortedDict

log = getLogger(__name__)


class AuditingSortedDict(SortedDict):
    def __init__(self, data=None, on_key_access_callable=None):
        super(AuditingSortedDict, self).__init__(data)
        self.on_key_access_callable = on_key_access_callable

    def _key_accessed(self, key):
        log.debug("Accessed key: %s" % (key,))
        if self.on_key_access_callable:
            self.on_key_access_callable(key)

    def items(self):
        items = super(AuditingSortedDict, self).items()
        for key, _ in items:
            self._key_accessed(key)
        return items

    def keys(self):
        keys = super(AuditingSortedDict, self).keys()
        for key in keys:
            self._key_accessed(key)
        return keys

    def iterkeys(self):
        for key in super(AuditingSortedDict, self).iterkeys():
            self._key_accessed(key)
            yield key

    def get(self, k, d=None):
        self._key_accessed(k)
        return super(AuditingSortedDict, self).get(k, d)

    def iteritems(self):
        for key, value in super(AuditingSortedDict, self).iteritems():
            self._key_accessed(key)
            yield (key, value)

    def __getitem__(self, y):
        self._key_accessed(y)
        return super(AuditingSortedDict, self).__getitem__(y)

