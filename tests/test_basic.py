from .. ldapy import Ldappy, User, Group


def test_authenticate(config):
    ldapy = Ldappy(config)
    assert ldapy.authenticate(config['username'], config['password'])


def test_authenticate_wrong_credentials(config):
    bad_config = config.copy()
    bad_config['username'] = 'not_exist'
    ldapy = Ldappy(bad_config)
    assert not ldapy.authenticate(bad_config['username'], bad_config['password'])


def test_get_all_users(config):
    ldapy = Ldappy(config)
    users = ldapy.user_objects.all()
    assert len(users) > 0


def test_get_user(config, user):
    ldapy = Ldappy(config)
    user = ldapy.user_objects.get(name=user)
    assert type(user) is User


def test_get_user_data(config, user):
    ldapy = Ldappy(config)
    user = ldapy.user_objects.get(name=user)
    assert len(user.pretty_data()) > 0


def test_get_none_exists_user(config):
    ldapy = Ldappy(config)
    user = ldapy.user_objects.get(name='not_exist')
    assert user is None


def test_get_user_groups(config, user):
    ldapy = Ldappy(config)
    user = ldapy.user_objects.get(name=user)
    assert len(user.groups()) > 0


def test_get_all_groups(config):
    ldapy = Ldappy(config)
    groups = ldapy.group_objects.all()
    assert len(groups) > 0
    for group in groups:
        assert type(group) is Group


def test_get_group(config, group):
    ldapy = Ldappy(config)
    group = ldapy.group_objects.get(name=group)
    assert type(group) is Group


def test_get_group_members(config, group):
    ldapy = Ldappy(config)
    users = ldapy.group_objects.members_of(name=group)
    for user in users:
        assert type(user) is User


def test_get_user_by_dn(config, group):
    ldapy = Ldappy(config)
    group = ldapy.group_objects.get(name=group)
    assert type(group) is Group
    for user in group.members():
        user = ldapy.user_objects.get(dn=user.distinguished_name)
        assert type(user) is User


def test_get_group_by_dn(config, user):
    ldapy = Ldappy(config)
    user = ldapy.user_objects.get(name=user)
    assert type(user) is User
    for group in user.groups():
        group = ldapy.group_objects.get(dn=group.distinguished_name)
        assert type(group) is Group
