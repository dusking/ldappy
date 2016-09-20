ldappy
======

[![Build Status](https://travis-ci.org/dusking/ldappy.svg?branch=master)](https://travis-ci.org/dusking/ldappy)
[![PypI](http://img.shields.io/pypi/v/ldappy.svg)](http://img.shields.io/pypi/v/ldappy.svg)

Why are there two p's in `ldappy` and not only one? you may ask.. well.. it's because it's the Happy way to use ldap with python :) `ldappy` gives api to query LDAP server, without the need to know about LDAP. Supporting both Active directory and open LDAP servers.


ldappy uses [pyldap](https://github.com/pyldap/pyldap) for the communication with the LDAP server. 

## Installation

```shell
pip install ldappy
```

## dev requirements

```shell
sudo apt-get install gcc, python-dev
sudo apt-get install python3-dev, libpython3-dev, libpython3.4-dev, libpython3.5-dev
python3.4 -m pip install pyldap
python3.5 -m pip install pyldap
```

## Usage

### Sample usage
```shell
ldappy = Ldappy(config)
all_users = ldappy.user_objects.all()
user = all_users[0]
print user.pretty_data()
```
You can see a full sample usage at samples/sample_usage.py or at the tests.

### Info
There is User object and Group object. Each of them inherit from dict, so all the relevant data can be seen easly. BUT, since there are some different field name convenstions between the Open LDAP and Active Directory, there is the pretty_data methos, which return the same data, but with common name convenstion.. for example, full_name insttead of fn..

## Testing

NOTE: Running the tests require an internet connection
NOTE: You may install some dependencies. 

```shell
git clone git@github.com:dusking/ldappy.git
cd ldappy
pip install tox
tox
```


