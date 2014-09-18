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
config_file = '/etc/mopidy/mopidy.conf'

#log_file = '/var/log/mopidy/mopidy.log'

password_mask = '******'

class Extension(ext.Extension):
    dist_name = 'Mopidy-WebSettings'
    ext_name = 'websettings'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['musicbox'] = config.String()
        schema['config_file'] = config.String()
        return schema

    def setup(self, registry):
        registry.add('http:app', {
            #'name': self.ext_name,
            'name': 'settings',
            'factory': websettings_app_factory,
        })

class WebSettingsRequestHandler(tornado.web.RequestHandler):

    def initialize(self, core):
        self.core = core

    def get(self):
        templateLoader = jinja2.FileSystemLoader( searchpath = "/" )
        templateEnv = jinja2.Environment( loader=templateLoader )
        template = templateEnv.get_template(template_file)
        error = ''
        #read config file
        try:
            iniconfig = ConfigObj(config_file, configspec=spec_file, file_error=True, encoding='utf8')
        except (ConfigObjError, IOError), e:
            error = 'Could not load ini file! %s %s %s', e, ConfigObjError, IOError
        #read values of valid items (in the spec-file)
        validItems = ConfigObj(spec_file, encoding='utf8')
        templateVars = {
            "error": error
        }
        #iterate over the valid items to get them into the template
        for item in validItems:
            for subitem in validItems[item]:
                itemName = item + '__' + subitem
                try:
                    configValue = iniconfig[item][subitem]
                    #compare last 8 caracters of subitemname
                    if subitem[-8:] == 'password' and configValue != '':
                        configValue = password_mask
                    templateVars[itemName] = configValue
                except:
                    pass
        self.write(template.render ( templateVars ) )

    def post(self):
        error = ''
        try:
            iniconfig = ConfigObj(config_file, configspec=spec_file, file_error=True, encoding='utf8')
        except (ConfigObjError, IOError), e:
            error = 'Could not load ini file!'
        validItems = ConfigObj(spec_file, encoding='utf8')
        templateVars = {
            "error": error
        }
        #iterate over the items, so that only valid items are processed
        for item in validItems:
            for subitem in validItems[item]:
                itemName = item + '__' + subitem
                argumentItem = self.get_argument(itemName)
                if argumentItem:
                    #don't edit config value if password mask
                    if subitem[-8:] == 'password':
                      if argumentItem == password_mask or argumentItem == '':
                          continue
                    iniconfig[item][subitem] = argumentItem
        iniconfig.write()
        logger.info('Rebooting system')
        #        os.system("sudo shutdown -r now")
        #        os.system("shutdown -r now")
        #        os.system("/opt/musicbox/startup.sh")
        self.write("<html><body><h1>Settings Saved!</h1><script>toast('Applying changes (reboot)...', 5000);setTimeout(function(){window.location.assign('/');}, 10000);</script><a href='/'>Back</a></body></html>")

def websettings_app_factory(config, core):
    config_file = config.get('websettings', 'config_file')
    return [
        ('/', WebSettingsRequestHandler, {'core': core})
    ]
