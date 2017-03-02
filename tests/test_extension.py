from __future__ import unicode_literals

import unittest

from mopidy_websettings import Extension


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = Extension()

        config = ext.get_default_config()

        self.assertIn('[websettings]', config)
        self.assertIn('enabled = true', config)

    def test_get_config_schema(self):
        ext = Extension()

        schema = ext.get_config_schema()

        self.assertIn('musicbox', schema)
        self.assertIn('config_file', schema)

    # TODO Write more tests
