import logging
from .group import Group
from .ldapquery import LdapQuery, LdapScope
from .connection import handle_ldap_connection

logger = logging.getLogger(__name__)


class Groups(LdapQuery):
    def __init__(self, *args, **kwargs):
        super(Groups, self).__init__(*args, **kwargs)
        self._group_filter = '(|(objectClass=group)(objectClass=groupOfNames))'

    @handle_ldap_connection
    def all(self, search_attribute=None):
        """
        :param search_attribute: list of attributes to retrieve for groups.
        :return: list of Groups - "dictionary" with returned attributes about the groups.
        """
        search_attribute = ["*"] if search_attribute is None else search_attribute
        search_attribute = search_attribute \
            if type(search_attribute) is list \
            else list(search_attribute)
        search_filter = self._group_filter
        base_dn = self._base_dn
        result = self.search(base_dn, LdapScope.SUBTREE, search_filter, search_attribute)
        if not result:
            logger.warning('Failed to retrieve all groups')
            return None
        groups = []
        for item in result:
            group_distinguished_name, group_info = item
            if group_distinguished_name:  # may be None..
                group_info.update({'group_dn': [group_distinguished_name]})
                groups.append(Group(group_info))
        return groups

    def get(self, name=None, dn=None, attribute=None):
        """
        :param name: group name we want to quest.
        :param dn: distinguished_name of group to quest.
        :param attribute: list of attributes to retrieve for the group. default: ['*']
        :return: Group object - "dictionary" with returned attributes about the group.
        """
        if not name and not dn:
            logger.error('missing parameter from user.get')
            return None
        attribute = ["*"] if attribute is None else attribute
        result = None
        if name:
            result = self._get_by_name(name, attribute)
        elif dn:
            result = self._get_by_dn(dn, attribute)
        result = self._remove_empty_items(result)
        if not result:
            logger.warning('Failed to find info for group: {0}'.format(name if name else dn))
            return None
        group_distinguished_name, group_info = result[0]
        return Group(group_info)

    @handle_ldap_connection
    def members_of(self, name):
        """
        This is a shortcut for the common task of retrieving members of specific group.
        :param name: the group common name we want to quest.
        :return: list of Users
        """
        group = self.get(name=name, attribute=['member'])
        if type(group) is not Group:
            return []
        return group.members()

    @handle_ldap_connection
    def _get_by_name(self, name, attribute=None):
        search_filter = "(&(cn={name}){group_filter})".format(name=name,
                                                              group_filter=self._group_filter)
        return self.search(self._base_dn, LdapScope.SUBTREE, search_filter, attribute)

    @handle_ldap_connection
    def _get_by_dn(self, dn, attribute=None):
        return self.search(dn, LdapScope.SUBTREE, self._group_filter, attribute)
