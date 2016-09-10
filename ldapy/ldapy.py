import logging
from .users import Users
from .groups import Groups
from .config import Config
from .ldapconnection import LdapConnection

logger = logging.getLogger(__name__)


class Ldapy(object):
    """
    Wrapper to the ldap lib, one that will make you happy.

    ldap docs: https://www.python-ldap.org/doc/html/ldap.html
    ldap docs references: https://www.python-ldap.org/docs.html
    ldap samples: http://www.grotan.com/ldap/python-ldap-samples.html
    """

    def __init__(self, config):
        self._ldap_config = Config(config)
        self._ldap_conn = None
        self._user_objects = Users(self._ldap_config)
        self._group_objects = Groups(self._ldap_config)

    def authenticate(self, username=None, password=None):
        connection = LdapConnection(self._ldap_config)
        try:
            connection.connect(username, password)
            result = True
        except:
            result = False
        connection.disconnect()
        return result

    @property
    def user_objects(self):
        return self._user_objects

    @property
    def group_objects(self):
        return self._group_objects
