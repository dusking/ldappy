import logging
from .ldapconfig import LdapConfig
from .users import Users
from .groups import Groups
from .ldapconnection import handle_ldap_connection

logger = logging.getLogger(__name__)


class Ldapy(object):
    """
    Wrapper to the ldap lib, one that will make you happy.

    ldap docs: https://www.python-ldap.org/doc/html/ldap.html
    ldap docs references: https://www.python-ldap.org/docs.html
    ldap samples: http://www.grotan.com/ldap/python-ldap-samples.html
    """

    def __init__(self, config):
        self._ldap_config = LdapConfig(config)
        self._ldap_conn = None
        self._user_objects = Users(self._ldap_config)
        self._group_objects = Groups(self._ldap_config)

    @handle_ldap_connection
    def authenticate(self, username=None, password=None):
        if username and password:
            pass
        return bool(self._ldap_conn)

    @property
    def user_objects(self):
        return self._user_objects

    @property
    def group_objects(self):
        return self._group_objects
