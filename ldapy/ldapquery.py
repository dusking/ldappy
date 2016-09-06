import logging
import ldap
from .safeldap import safe_ldap

logger = logging.getLogger(__name__)
LDAP_SUCCESS_CODE = 97


def byte_to_str(obj):
    if type(obj) is not list:
        return
    for index, _ in enumerate(obj):
        if type(obj[index]) is tuple:
            obj[index] = list(obj[index])
        if type(obj[index]) is list:
            byte_to_str(obj[index])
            return
        if type(obj[index]) is dict:
            for key, value in obj[index].items():
                byte_to_str(obj[index][key])
            return
        if type(obj[index]) is bytes:
            try:
                obj[index] = obj[index].decode("utf-8")
            except:
                obj[index] = str(obj[index])


class LdapScope(object):
    BASE = ldap.SCOPE_BASE
    ONE = ldap.SCOPE_ONELEVEL
    SUBTREE = ldap.SCOPE_SUBTREE


class LdapQuery(object):
    """
    Handle the queries to the LDAP server. Some info about LDAP search parameters:

    Base DN: The base distinguished name (DN)
    indicates where in the LDAP directory you wish to begin the search.
    An LDAP directory is arranged in tree fashion, with a root and various branches off this root.
    The base DN is used to indicate at which node the search should originate.
    For example, we could indicate a base of dc=idevelopment,dc=info
    for a search that starts at the top and proceeds downward.
    If instead we specified dc=idevelopment,dc=info
    then any entries above this tree would not be eligible for searching.

    Scope: It is the stating point of a search and the depth
    from the base DN to which the search should occur.
    There are three options (values) for the scope:
     - BASE: Is used to indicate searching only the entry at the base DN,
        resulting in only that entry being returned
        (if it also meets the search filter criteria).
     - ONE: Is used to indicate searching all entries one level under the base DN -
        but NOT including the base DN.
     - SUBTREE: Is used to indicate searching of all entries at all levels
        under and including the specified base DN.

    Filter: The search filter is the query string.
    It is used to filter the entries in the directory
    and produce the desired set of matching records.
    Filters are built using parentheses and combinations of the symbols:
    &, |, and !, which represent AND, OR and NOT.
    If you wanted to locate all people with "jhunter" at the beginning of their names,
    the following filter would do the trick: (&(objectclass=person)(cn=jhunter*))
    """
    def __init__(self, ldap_config):
        self._ldap_config = ldap_config
        self._ldap_conn = None
        organization_id = 'o={0},'.format(self._ldap_config.organization_id) \
            if self._ldap_config.organization_id \
            else ''
        self._base_dn = '{0}{1}'.format(organization_id, self._ldap_config.domain_component)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

        self.search = self.search_sync

    @safe_ldap(default=None, message='Failed to query ldap server')
    def search_async(self,
                     base_dn,
                     search_scope,
                     search_filter='(objectClass=*)',
                     attribute_list=None,
                     attrs_only=0):
        """
        The main operation for reading a directory, is the LDAP search operation.
        This is the not synchronous form of the search.
        :param base_dn: indicates where in the directory information tree the search should start.
        :param search_scope: indicates how deeply the search should delve into the directory tree.
        :param search_filter: indicates which entries should be considered matches.
        :param attribute_list: indicates which attributes of a matching record should be returned.
        :param attrs_only: A flag indicating whether attribute values should be returned
        :return: LDAP search operation result.
        """
        logger.debug('new async query [server: {0}, base: {1}, filter: {2}]'
                     .format(self._ldap_config.ldap_server,
                             base_dn,
                             search_filter))
        result_id = self._ldap_conn.search(base=base_dn,
                                           scope=search_scope,
                                           filterstr=search_filter,
                                           attrlist=attribute_list,
                                           attrsonly=attrs_only)
        result_set = []
        while 1:
            result_type, result_data = self._ldap_conn.result(result_id, 0)
            if not result_data:
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        byte_to_str(result_set)
        return result_set

    @safe_ldap(default=None, message='Failed to query ldap server')
    def search_sync(self,
                    base_dn,
                    search_scope,
                    search_filter='(objectClass=*)',
                    attribute_list=None,
                    attrs_only=0,
                    timeout_sec=-1):
        """
        The main operation for reading a directory, is the LDAP search operation.
        This is the synchronous form of the search.
        :param base_dn: indicates where in the directory information tree the search should start.
        :param search_scope: indicates how deeply the search should delve into the directory tree.
        :param search_filter: indicates which entries should be considered matches.
        :param attribute_list: indicates which attributes of a matching record should be returned.
        :param attrs_only: A flag indicating whether attribute values should be returned
        :param timeout_sec: if the server takes longer than timeout, the search is aborted.
                -1 fot infinite time.
        :return: LDAP search operation result.
        """
        logger.debug('new query [server: {0}, base: {1}, filter: {2}]'
                     .format(self._ldap_config.ldap_server,
                             base_dn,
                             search_filter))
        result = self._ldap_conn.search_st(base=base_dn,
                                           scope=search_scope,
                                           filterstr=search_filter,
                                           attrlist=attribute_list,
                                           attrsonly=attrs_only,
                                           timeout=timeout_sec)
        byte_to_str(result)
        return result

    @staticmethod
    def _remove_empty_items(list_input):
        """
        :param list_input: list of tuples
        :return: the input list, without tuples with None at first field
        """
        result = []
        if type(list_input) is not list:
            return result
        for item in list_input:
            if item[0]:
                result.append(item)
        return result
