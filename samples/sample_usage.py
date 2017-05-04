#!/usr/bin/python

# This file is part of ldapy.
#
# ldapy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ldapy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ldapy.  If not, see <http://www.gnu.org/licenses/>.

import logging
from ldappy import Ldappy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

jumpcloud_config = {'ldap_server': 'ldap://ldap.jumpcloud.com/',
                    'domain_component': 'dc=jumpcloud,dc=com',
                    'organization_id': '57bd7a8df6978662316e998e',
                    'username': 'domer',
                    'password': '!QAZ2wsx'}

config = {'ldap_server': 'ldap://52.57.52.159:389/',
          'active_directory': True,
          'domain': 'cloudify.com',
          'username': 'omer1',
          'password': '!QAZ2wsx'}

def set_logger():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    ldapylogger = logging.getLogger('ldapy')
    ldapylogger.setLevel(logging.DEBUG)
    ldapylogger.addHandler(handler)


def get_group():
    logger.debug('get group info')
    ldapy = Ldappy(jumpcloud_config)
    group = ldapy.group_objects.get('group2')
    group.pretty_print()


if __name__ == "__main__":
    set_logger()
    get_group()
