"""Tests for certbot_dns_nsone._internal.dns_nsone."""

import unittest

import mock
from requests.exceptions import HTTPError

from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.tests import util as test_util

API_KEY = 'foo'


class AuthenticatorTest(test_util.TempDirTestCase,
                        dns_test_common_lexicon.BaseLexiconAuthenticatorTest):

    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        from certbot_dns_nsone._internal.dns_nsone import Authenticator

        path = os.path.join(self.tempdir, 'file.ini')
        dns_test_common.write({"nsone_api_key": API_KEY}, path)

        self.configure(Authenticator(self.config, "nsone"), {"credentials": path})

        self.mock_client = mock.MagicMock()
        # _get_nsone_client | pylint: disable=protected-access
        self.auth._get_nsone_client = mock.MagicMock(return_value=self.mock_client)


class NS1LexiconClientTest(unittest.TestCase, dns_test_common_lexicon.BaseLexiconClientTest):
    def domain_not_found(self, domain):
        return HTTPError('404 Client Error: Not Found for url: {0}.'.format(domain))

    def login_error(self, domain):
        return HTTPError('401 Client Error: Unauthorized for url: {0}.'.format(domain))

    def setUp(self):
        from certbot_dns_nsone._internal.dns_nsone import _NS1LexiconClient

        self.client = _NS1LexiconClient(API_KEY, 0)

        self.provider_mock = mock.MagicMock()
        self.client.provider = self.provider_mock


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
