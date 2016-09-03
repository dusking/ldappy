# content of conftest.py


def pytest_addoption(parser):
    parser.addoption("--ad", action="store_true", help="run on active directory")
    parser.addoption("--ldap", action="store_true", help="run on active directory")
    parser.addoption("--fox", action="store_true", help="run on active directory")


def pytest_generate_tests(metafunc):
    configs = {'ad_config': {'config': {'ldap_server': 'ldap://52.57.5.220:389/',
                                        'organization_id': '',
                                        'active_directory': True,
                                        'domain': 'cloudify.com',
                                        'domain_component': 'dc=cloudify,dc=com',
                                        'username': 'omer',
                                        'password': '!QAZ2wsx'},
                             'user': 'omer',
                             'group': 'group_1'},
               'jumpcloud_config': {'config': {'ldap_server': 'ldap://ldap.jumpcloud.com/',
                                               'domain_component': 'dc=jumpcloud,dc=com',
                                               'organization_id': '57bd7a8df6978662316e998e',
                                               'username': 'domer',
                                               'password': '!QAZ2wsx'},
                                    'user': 'domer',
                                    'group': 'group2'},
               }

    all_configs = False
    if not metafunc.config.option.ad and \
            not metafunc.config.option.ldap and \
            not metafunc.config.option.fox:
        all_configs = True
    if 'user' in metafunc.fixturenames:
        if metafunc.config.option.ad or all_configs:
            metafunc.addcall(funcargs={'config': configs['ad_config']['config'],
                                       'user': configs['ad_config']['user']})
        if metafunc.config.option.ldap or all_configs:
            metafunc.addcall(funcargs={'config': configs['jumpcloud_config']['config'],
                                       'user': configs['jumpcloud_config']['user']})
    elif 'group' in metafunc.fixturenames:
        if metafunc.config.option.ad or all_configs:
            metafunc.addcall(funcargs={'config': configs['ad_config']['config'],
                                       'group': configs['ad_config']['group']})
        if metafunc.config.option.ldap or all_configs:
            metafunc.addcall(funcargs={'config': configs['jumpcloud_config']['config'],
                                       'group': configs['jumpcloud_config']['group']})
    else:
        if metafunc.config.option.ad or all_configs:
            metafunc.addcall(funcargs={'config': configs['ad_config']['config']})
        if metafunc.config.option.ldap or all_configs:
            metafunc.addcall(funcargs={'config': configs['jumpcloud_config']['config']})
