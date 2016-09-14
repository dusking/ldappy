import logging
import ldap

logger = logging.getLogger(__name__)
LDAP_SUCCESS_CODE = 97


class LdapConnection(object):
    def __init__(self, config):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self._config = config
        self._conn = None

    def connection_login_string(self, user=None):
        username = user if user else self._config.username
        if self._config.active_directory:
            logger.debug('using active directory login style')
            logon_user = '{0}@{1}'.format(username, self._config.domain)
            return logon_user
        organization_id = ',o={0}'.format(self._config.organization_id) \
            if self._config.organization_id \
            else ''
        distinguished_name = 'uid={0},ou=Users{1},{2}'.format(username,
                                                              organization_id,
                                                              self._config.domain_component)
        return distinguished_name

    def connect(self, username=None, password=None):
        """
        :param username: existing username with permissions to bind to and search the LDAP service
        :param password: the user password
        :return: LDAPObject instance by opening LDAP connection to LDAP host specified by LDAP URL.
        """
        try:
            self._conn = ldap.initialize(self._config.ldap_server)
            self._conn.protocol_version = ldap.VERSION3
            self._conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            self._conn.set_option(ldap.OPT_REFERRALS, 0)
            distinguished_login_name = self.connection_login_string(username)
            password = password if password else self._config.password
            logger.debug('going to connect using user: {0}'.format(distinguished_login_name))
            result = self._conn.simple_bind_s(distinguished_login_name, password)
            if result[0] != LDAP_SUCCESS_CODE:
                raise ldap.LDAPError('LDAP user bind failed')
            return self._conn
        except ldap.INVALID_CREDENTIALS:
            raise Exception("Your username or password is incorrect: [user: {0}]"
                            .format(self._config.username))
        except ldap.LDAPError as e:
            error_msg = []
            if type(e.message) is dict:
                for (k, v) in e.message.iteritems():
                    error_msg.append("%s: %sn" % (k, v))
            else:
                error_msg.append(e.message)
            raise Exception(error_msg)

    def disconnect(self):
        """"
        Safely disconnect from the LDAP server
        """
        if self._conn:
            try:
                self._conn.unbind_s()
            except:
                pass