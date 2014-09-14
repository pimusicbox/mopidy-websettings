from __future__ import unicode_literals

import logging
import os

import tornado.web

from mopidy import config, ext

from configobj import ConfigObj, ConfigObjError
from validate import Validator
import jinja2

__version__ = '0.1.0'

# TODO: If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)

spec_file = os.path.join(os.path.dirname(__file__), 'settingsspec.ini')
template_file = os.path.join(os.path.dirname(__file__), 'index.html')
#log_file = '/var/log/mopidy/mopidy.log'
password_mask = '******'

class Extension(ext.Extension):
    dist_name = 'Mopidy-WebSettings'
    ext_name = 'settings'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['musicbox'] = config.String()
#        config_file = '/boot/config/settings.ini')
        schema['config_file'] = config.String()
        return schema

    def setup(self, registry):
        # TODO: Edit or remove entirely
        registry.add('http:static', {
            'name': self.ext_name,
            'factory': settings_app_factory,
        })

class SettingsRequestHandler(tornado.web.RequestHandler):
    def initialize(self, core):
        self.core = core

    def get(self):
        self.write(
            'Hello, world! This is Mopidy %s' %
            self.core.get_version().get())


def settings_app_factory(config, core):
    return [
        ('/', SettingsRequestHandler, {'core': core})
    ]
    