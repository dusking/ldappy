import logging
import ldap

logger = logging.getLogger(__name__)


class safe_ldap:
    _conn = None

    def __init__(self, default=None, message=None):
        self._default = default
        self._message = message

    def __call__(self, call):
        def _run(*args, **kwargs):
            try:
                return call(*args, **kwargs)
            except ldap.TIMEOUT as e:
                logger.error('the server took too long to respond, error: {0}'.format(e),
                             exc_info=True)
            except ldap.NO_SUCH_OBJECT as e:
                logger.error('unable to search on LDAP server, error: {0}'.format(e),
                             exc_info=True)
            except ldap.LDAPError as e:
                if type(e.message) == dict and 'desc' in e.message:
                    logger.error(e.message['desc'],
                                 exc_info=True)
                else:
                    logger.error(e,
                                 exc_info=True)
            except Exception as e:
                logger.error(e,
                             exc_info=True)
            return self._default

        return _run
