import logging
logger = logging.getLogger(__name__)


class DotExDict(dict):
    """
    DotExDict is a dotted extended version of the dict class.
    It allows both accessing values by dot notation (access dict keys as attributes),
    and to extend the attributes/keys by aliases.
    """

    def __init__(self, *args, **kwargs):
        super(DotExDict, self).__init__(*args, **kwargs)
        self._attributes_aliases = {}

    def __getattr__(self, attr):
        return self[attr]

    def __getitem__(self, key):
        if key in self:
            return super(DotExDict, self).__getitem__(key)
        if key in self._attributes_aliases:
            return getattr(self, self._attributes_aliases[key])
        return None

    def get(self, key, default=None):
        if key in self:
            return super(DotExDict, self).get(key, default)
        if hasattr(self, key):
            return getattr(self, key)
        return default

    def __setattr__(self, attr, value):
        self[attr] = value

    __delattr__ = dict.__delitem__

    def set_attribute_aliases(self, aliases):
        for alias, attribute in aliases.items():
            if attribute in self:
                self._attributes_aliases[alias] = attribute

dotexdict = DotExDict
