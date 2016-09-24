import re
import ldap
import logging

from IPy import IP

from .dotexdict import dotexdict

logger = logging.getLogger(__name__)


class Config(dotexdict):

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.set_attribute_aliases({
            'host_name': 'ldap_server',
            'ad_server': 'ldap_server',
            'active_directory_server': 'ldap_server',
            'windows_login_name': 'sam_account_name'
        })
        self._validate()
        self._set_domain_component()

    def _validate(self):
        required_attributes = ['username', 'password', 'ldap_server']
        for item in required_attributes:
            self._validate_key(item)

    def _validate_key(self, key):
        if key not in self:
            raise Exception('missing "{0}" in ldap configuration'.format(key))
        if not self[key]:
            raise Exception('missing value for "{0}" in ldap configuration'.format(key))

    def _add_ldap_port_to_server(self):
        """
        Add ldap por if missing.
        The standard port for LDAP is port 389 for non-SSL connections and 636 for SSL connections.
        :return:
        """
        if len(self.ldap_server.split(':')) < 3:
            self.ldap_server = '{0}:{1}/'.format(self.ldap_server.strip('/'), ldap.PORT)
            logger.info('adding ldap port to server: {0}'.format(self.ldap_server))

    def _set_domain_component(self):
        """
        If missing, add domain component to configuration based on the server url
        :return:
        """
        if 'domain_component' not in self:
            if not self._auto_create_domain_component():
                raise Exception('Missing domain_component in configuration')

    def _auto_create_domain_component(self):
        if 'domain' in self:
            domain_components = self.domain.split('.')
            self.domain_component = ','.join(['dc={0}'.format(dc) for dc in domain_components])
            logger.info('adding domain component: {0}, based on domain'
                        .format(self.domain_component))
            return True
        elif self._server_given_as_dns(self.ldap_server):
            ldap_server_without_port = re.sub(r':\d+/', '', self.ldap_server)
            components_list = ldap_server_without_port.split('.')
            dc_list = ['dc={0}'.format(dc) for dc in components_list[1:]]
            self.domain_component = ','.join(dc_list)
            logger.info('adding domain component: {0}, based on server'
                        .format(self.domain_component))
            return True
        return False

    @staticmethod
    def _server_given_as_dns(server_addr):
        try:
            only_ip = server_addr.replace('ldap://', '').strip('/')
            IP(only_ip)
            return False
        except:
            return True
