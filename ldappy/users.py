import logging
from .user import User
from .ldapquery import LdapQuery, LdapScope
from .connection import handle_ldap_connection

logger = logging.getLogger(__name__)


class Users(LdapQuery):
    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self._class_filter = "(|(objectClass=person)(objectClass=user))"

    @handle_ldap_connection
    def all(self, attribute=None):
        """
        :param attribute: list of attributes to retrieve for users.
        :return: list of Users - dictionary with returned attributes about the users.
        """
        attribute = attribute if attribute else ["*"]
        result = self.search(self._base_dn, LdapScope.SUBTREE, self._class_filter, attribute)
        if not result:
            logger.warning('Failed to retrieve users')
            return None
        users = []
        for item in result:
            user_distinguished_name, user_info = item
            if type(user_info) is not dict:
                continue
            user_info.update({'user_dn': [user_distinguished_name]})
            users.append(User(user_info))
        return users

    def get(self, name=None, dn=None, attribute=None):
        """
        :param name: username we want to quest.
        :param dn: distinguished_name of user to quest.
        :param attribute: list of attributes to retrieve for the user.
        :return: User object - "dictionary" with returned attributes about the user.
        """
        if not name and not dn:
            logger.error('missing parameter from user.get')
            return None
        attribute = attribute if attribute else ["*"]
        result = None
        if name:
            result = self._get_by_name(name, attribute)
        elif dn:
            result = self._get_by_dn(dn, attribute)
        result = self._remove_empty_items(result)
        if not result:
            logger.warning('Failed to find info for user: {0}'.format(name if name else dn))
            return None
        user_distinguished_name, user_info = result[0]
        return User(user_info)

    @handle_ldap_connection
    def _get_by_name(self, name, attribute=None):
        user_filter = '(|(sAMAccountName={user})(uid={user}))'.format(user=name)
        search_filter = "(&{class_filter}{user_filter})".format(class_filter=self._class_filter,
                                                                user_filter=user_filter)
        return self.search(self._base_dn, LdapScope.SUBTREE, search_filter, attribute)

    @handle_ldap_connection
    def _get_by_dn(self, dn, attribute=None):
        return self.search(dn, LdapScope.SUBTREE, self._class_filter, attribute)
