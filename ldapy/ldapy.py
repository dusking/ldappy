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

    def authenticate(self, username=None, password=None, retries=1):
        connection = LdapConnection(self._ldap_config)
        success = False
        try_to_connect = True
        while try_to_connect:
            logger.debug('Authentication attempt for user: {0}'.format(username))
            try:
                connection.connect(username, password)
                success = True
            except Exception as ex:
                logger.error('Authentication failed with error: {0}'.format(ex))
            retries -= 1
            try_to_connect = not success and retries > 0
        connection.disconnect()
        return success

    @property
    def user_objects(self):
        return self._user_objects

    @property
    def group_objects(self):
        return self._group_objects
