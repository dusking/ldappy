import logging
from .ldapconnection import LdapConnection

logger = logging.getLogger(__name__)
LDAP_SUCCESS_CODE = 97


class HandleLdapConnection(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __get__(self, instance, owner):
        wrapped = self.wrapped.__get__(instance, owner)
        return BoundFunctionWrapper(wrapped, instance)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


class BoundFunctionWrapper(object):
    def __init__(self, wrapped, instance):
        if not hasattr(instance, '_ldap_config'):
            raise Exception('missing _ldap_config parameter')
        if not hasattr(instance, '_ldap_conn'):
            raise Exception('missing _ldap_conn parameter')
        self.wrapped = wrapped
        self._default = None
        self._caller = instance

    def __call__(self, *args, **kwargs):
        result = self._default
        try:
            self._config = self._caller._ldap_config
            self._ldap_connection = LdapConnection(self._config)
            self._caller._ldap_conn = None
            self._caller._ldap_conn = self._ldap_connection.connect()
            result = self.wrapped(*args, **kwargs)
        except Exception as e:
            logger.error('wrapped function "{0}" failed or was not called: {1}'
                         .format(self.wrapped.__name__, e))
        self._ldap_connection.disconnect()
        return result

handle_ldap_connection = HandleLdapConnection
