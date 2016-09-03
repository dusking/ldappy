import logging
import ldap

logger = logging.getLogger(__name__)
LDAP_SUCCESS_CODE = 97


class HandleLdapConnection(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

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
        self._conn = None
        self._caller_self = instance

    def __call__(self, *args, **kwargs):
        result = self._default
        try:
            self._caller_self._ldap_conn = None
            self._config = self._caller_self._ldap_config
            self.connect()
            self._caller_self._ldap_conn = self._conn
            result = self.wrapped(*args, **kwargs)
        except Exception as e:
            logger.error('wrapped function "{0}" failed or was not called: {1}'
                         .format(self.wrapped.__name__, e))
        self.disconnect()
        return result

    def connection_login_string(self):
        if self._config.active_directory:
            logger.debug('using active directory login style')
            logon_user = '{0}@{1}'.format(self._config.username, self._config.domain)
            return logon_user
        organization_id = ',o={0}'.format(self._config.organization_id) \
            if self._config.organization_id \
            else ''
        distinguished_name = 'uid={0},ou=Users{1},{2}'.format(self._config.username,
                                                              organization_id,
                                                              self._config.domain_component)
        return distinguished_name

    def connect(self):
        """
        :param user: existing username with permissions to bind to and search the LDAP service
        :param password: the user password
        :param ldap_server:
        :return:  LDAPObject instance by opening LDAP connection to LDAP host specified by LDAP URL.
        """
        try:
            self._conn = ldap.initialize(self._config.ldap_server)
            self._conn.protocol_version = ldap.VERSION3
            self._conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            self._conn.set_option(ldap.OPT_REFERRALS, 0)
            distinguished_login_name = self.connection_login_string()
            logger.debug('going to connect using user: {0}'.format(distinguished_login_name))
            result = self._conn.simple_bind_s(distinguished_login_name, self._config.password)
            return result[0] == LDAP_SUCCESS_CODE
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

handle_ldap_connection = HandleLdapConnection
