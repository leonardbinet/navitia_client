import unittest
import codecs

try:  # Python 3
    from urllib.parse import urlparse, parse_qsl
except ImportError:  # Python 2
    from urlparse import urlparse, parse_qsl


class TestCase(unittest.TestCase):

    def assertURLEqual(self, first, second, msg=None):
        """Check that two arguments are equivalent URLs. Ignores the order of
        query arguments.
        """
        first_parsed = urlparse(first)
        second_parsed = urlparse(second)
        self.assertEqual(first_parsed[:3], second_parsed[:3], msg)

        first_qsl = sorted(parse_qsl(first_parsed.query))
        second_qsl = sorted(parse_qsl(second_parsed.query))
        self.assertEqual(first_qsl, second_qsl, msg)

    def u(self, string):
        """Create a unicode string, compatible across all versions of Python."""
        # NOTE: Python 3-3.2 does not have the u'' syntax.
        return codecs.unicode_escape_decode(string)[0]
