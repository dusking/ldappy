# -*- coding: utf-8 -*-
import re
import pprint
from .dotexdict import dotexdict


class LdapObject(dotexdict):

    def __init__(self, *args, **kwargs):
        super(LdapObject, self).__init__(*args, **kwargs)

    def pretty_data(self):
        """
        :return: dict with selected attributes - that in self._print_attributes
        """
        result = {}
        for key in self._print_attributes:
            try:
                assert isinstance(key, str)
                if type(self[key]) is not list:
                    self[key] = [self[key]]
                value = [str(value) for value in self[key]]
                result[key] = value
            except:
                pass
        return result

    def pretty_print(self):
        """
        pretty print of the pretty data
        """
        print (self.pretty_data())
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.pretty_data())

    def _extract_keys_from_dn(self, keys, distinguish_name):
        """
        :param keys: list of keys to extract from the dn
        :param distinguish_name: DN we want to extract fields from
        :return: list of fields (keys) extracted from the DN
        """
        result = []
        dn = self._dn_to_dict(distinguish_name.lower())
        for key in keys:
            if key in dn:
                result.append(dn[key])
        return result

    def _extract_keys_from_list_of_dn(self, keys, distinguish_names):
        """
        :param keys: list of keys to extract from the dn
        :param distinguish_names: list of distinguish names (DN)
        :return: list of fields (keys) extracted from the DN
        """
        result = []
        for dn_str in distinguish_names:
            extracted_keys = self._extract_keys_from_dn(keys, dn_str)
            if extracted_keys:
                result.append(extracted_keys)
        return result

    def _dn_to_dict(self, dn):
        """
        :param dn: distinguish names (DN) string
        :return: dict representing the DN data (keys and values)
        """
        return dict((key, value) for key, value in (item.split('=') for item in dn.split(',')))

    def _aliases_to_cammelcase(self, attributes):
        """
        :param attributes: list of attributes in CamelCase format
        :return: dictionary of desire aliases - snake_case format alias to CamelCase
        """
        result = {}
        for attr in attributes:
            result[self._cammelcase_to_snakecase(attr)] = attr
        return result

    def _cammelcase_to_snakecase(self, camelcase):
        """
        :param camelcase: attribute name in CamelCase format
        :return: the attribute in snake_case format
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camelcase)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
