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

####
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def updateSettings(self, **params):
        error = ''
        try:
            config = ConfigObj(config_file, configspec=spec_file, file_error=True)
        except (ConfigObjError, IOError), e:
            error = 'Could not load ini file!'
#        print (params)
        validItems = ConfigObj(spec_file)
        templateVars = {
            "error": error
        }
        #iterate over the items, so that only valid items are processed
        for item in validItems:
            for subitem in validItems[item]:
                itemName = item + '__' + subitem
#                print itemName
                if itemName in params.keys():
                    #don't edit config value if password mask
                    if subitem[-8:] == 'password':
                      if params[itemName] == password_mask:
                          continue
                    config[item][subitem] = params[itemName]
#                    print params[itemName]
        config.write()
        logger.info('Rebooting system')
        os.system("sudo shutdown -r now")
        os.system("shutdown -r now")
#        os.system("/opt/musicbox/startup.sh")
        return "<html><body><h1>Settings Saved!</h1><script>toast('Applying changes (reboot)...', 5000);setTimeout(function(){window.location.assign('/');}, 10000);</script><a href='/'>Back</a></body></html>"

    @cherrypy.expose
    def Settings(self, **params):
        templateLoader = jinja2.FileSystemLoader( searchpath = "/" )
        templateEnv = jinja2.Environment( loader=templateLoader )
        template = templateEnv.get_template(template_file)
        error = ''
        #read config file
        try:
            config = ConfigObj(config_file, configspec=spec_file, file_error=True)
        except (ConfigObjError, IOError), e:
            error = 'Could not load ini file! %s %s %s', e, ConfigObjError, IOError
#        print (error)
        #read values of valid items (in the spec-file)
        validItems = ConfigObj(spec_file)
        templateVars = {
            "error": error
        }
        #iterate over the valid items to get them into the template
        for item in validItems:
#            print(item)
            for subitem in validItems[item]:
#                print('['+subitem)
                itemName = item + '__' + subitem
                try:
                    configValue = config[item][subitem]
                    #compare last 8 caracters of subitemname
                    if subitem[-8:] == 'password':
                        configValue = password_mask
                    templateVars[itemName] = configValue
                except:
                    pass
#        print templateVars
        return template.render ( templateVars )

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def haltSystem(self, **params):
        logger.info('Halting system')
        os.system("sudo shutdown -h now")
        os.system("shutdown -h now")

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def rebootSystem(self, **params):
        logger.info('Rebooting system')
        os.system("sudo shutdown -r now")
        os.system("shutdown -r now")

    @cherrypy.expose
    def log(self, **params):
        page = '<html><body><h2>MusicBox/Mopidy Log (can take a while to load...)</h2><pre>'
        with open(log_file, 'r') as f:
            page += f.read()
            page += '</pre></body></html>'
        return page
