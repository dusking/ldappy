# -*- coding: utf-8 -*-
from . import group
from .ldapobject import LdapObject


class User(LdapObject):

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._create_attribute_aliases()
        self._print_attributes = list(self._attributes_aliases.keys())
        self._print_attributes.extend(['mail',
                                       'department',
                                       'description',
                                       'company',
                                       'title',
                                       'manager'])

    def groups(self):
        if 'memberOf' not in self:
            return []
        result = []
        for member in self.memberOf:
            result.append(group.Group({'cn': self._extract_keys_from_dn(keys=['cn'],
                                                                        distinguish_name=member),
                                       'distinguishedName': member}))
        return result

    def _create_attribute_aliases(self):
        self.set_attribute_aliases({
            'full_name': 'cn',
            'first_name': 'givenName',
            'last_name': 'sn',
            'country': 'co',
            'country_code': 'c',
            'logon': 'userPrincipalName'
        })
        self.set_attribute_aliases({'username': 'sAMAccountName'}) if 'sAMAccountName' in self \
            else self.set_attribute_aliases({'username': 'uid'})
        self.set_attribute_aliases(self._aliases_to_cammelcase(['displayName',
                                                                'distinguishedName',
                                                                'objectCategory',
                                                                'objectClass',
                                                                'homeDirectory',
                                                                'directReports',
                                                                'memberOf']))
