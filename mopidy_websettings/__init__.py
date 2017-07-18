from __future__ import unicode_literals

import logging
import os
import sys


from configobj import ConfigObj, ConfigObjError

import jinja2

from mopidy import config, ext

import tornado.web

__version__ = '0.2.0'

logger = logging.getLogger(__name__)

spec_file = os.path.join(os.path.dirname(__file__), 'settingsspec.ini')
template_file = os.path.join(os.path.dirname(__file__), 'index.html')


def mask(password):
    return '*' * len(password)


def restart_program():
    """
    DOES NOT WORK WELL WITH MOPIDY
    Hack from
    https://www.daniweb.com/software-development/python/code/260268/restart-your-python-program
    to support updating the settings, since mopidy is not able to do that yet
    Restarts the current program
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function
    """

    python = sys.executable
    os.execl(python, python, * sys.argv)


class Extension(ext.Extension):
    dist_name = 'Mopidy-WebSettings'
    ext_name = 'websettings'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['musicbox'] = config.Boolean()
        schema['config_file'] = config.String()
        return schema

    def setup(self, registry):
        registry.add('http:app', {
            # 'name': self.ext_name,
            'name': 'settings',
            'factory': websettings_app_factory,
        })


class WebSettingsRequestHandler(tornado.web.RequestHandler):

    def initialize(self, config):
        self.config_file = config['websettings']['config_file']

    def get(self):
        templateLoader = jinja2.FileSystemLoader(searchpath="/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(template_file)
        error = ''

        # Read config file
        try:
            iniconfig = ConfigObj(self.config_file, configspec=spec_file,
                                  file_error=True, encoding='utf8')
        except (ConfigObjError, IOError) as e:
            error = 'Could not load ini file! %s' % e
            logger.error(error)

        templateVars = {'error': error}
        # Read values of valid items (in the spec-file)
        validItems = ConfigObj(spec_file, encoding='utf8')
        # Iterate over the valid items to get them into the template
        for item in validItems:
            for subitem in validItems[item]:
                itemName = item + '__' + subitem
                try:
                    configValue = iniconfig[item][subitem]
                    if subitem.endswith('password') and configValue:
                        configValue = mask(configValue)
                    templateVars[itemName] = configValue
                except:
                    pass

        self.write(template.render(templateVars))


class WebPostRequestHandler(tornado.web.RequestHandler):

    def initialize(self, config):
        self.config_file = config.get('websettings')['config_file']

    def needs_reboot(self, item, subItem):
        reboot_sections = ['network', 'musicbox']
        restart_subsections = ['webclient']
        if item in reboot_sections:
            # Restarting Mopidy is sufficient for some subsections.
            if subItem not in restart_subsections:
                return True
        return False

    def post(self):
        apply_html = ''
        apply_string = 'restart Mopidy'
        status = ''
        try:
            iniconfig = ConfigObj(self.config_file, configspec=spec_file,
                                  file_error=True, encoding='utf8')
            validItems = ConfigObj(spec_file, encoding='utf8')
            # Iterate over the items, so that only valid items are processed
            for item in validItems:
                for subitem in validItems[item]:
                    itemName = item + '__' + subitem

                    value = self.get_argument(itemName, default='')
                    if value:
                        # Skip any masked passwords
                        if subitem.endswith('password') and \
                                value == mask(value):
                            continue
                        # Create default entry if it doesn't already exist
                        oldItem = iniconfig.setdefault(item, {}).setdefault(
                            subitem, '')
                        # Does changing the setting requires a system reboot.
                        if oldItem != value and \
                                self.needs_reboot(item, subitem):
                            apply_string = 'reboot system'
                        iniconfig[item][subitem] = value
            # Ensure the alsamixer and audio/mixer settings are consistent.
            try:
                if iniconfig['audio']['mixer'] == 'alsamixer':
                    iniconfig['alsamixer']['enabled'] = 'true'
                else:
                    iniconfig['alsamixer']['enabled'] = 'false'
            except:
                pass

            iniconfig.write()
            status = 'Settings Saved!'
            apply_html = ('<form action="apply" method="post">'
                          '<input type="submit" name="method" '
                          'value="Apply changes now (' + apply_string + ')" />'
                          )
        except (ConfigObjError, IOError) as e:
            status = 'Could not load ini file! %s' % e
            logger.error(status)

        message = ('<html>'
                   '<body>'
                   '<h1>' + status + '</h1>'
                   '<p>' + apply_html +
                   '<br/><br/>'
                   '<a href="/">Home</a>'
                   '<br/></p>'
                   '</body>'
                   '</html>')
        self.write(message)


class WebApplyRequestHandler(tornado.web.RequestHandler):

    def initialize(self): pass

    def post(self):
        method = self.get_argument('method', None)
        if method is not None:
            if 'reboot' in method:
                status = 'Rebooting Musicbox system...'
                os.system("sudo shutdown -r now")
            elif 'restart' in method:
                status = 'Restarting Mopidy service...'
                os.system("sudo /etc/init.d/mopidy restart")
            else:
                status = 'Error while applying ' + method
        logger.info(status)
        message = ('<html>'
                   '<body>'
                   '<h1>' + status + '</h1>'
                   '<br/><br/>'
                   '<a href="/">Home</a>'
                   '<br/></p>'
                   '</body>'
                   '</html>')
        self.write(message)


class WebRebootRequestHandler(tornado.web.RequestHandler):

    def initialize(self): pass

    def post(self):
        logger.info('Halting system')
        os.system("sudo shutdown -r now")
        os.system("shutdown -r now")


class WebShutdownRequestHandler(tornado.web.RequestHandler):

    def initialize(self): pass

    def post(self):
        logger.info('Halting system')
        os.system("sudo shutdown -h now")
        os.system("shutdown -h now")


def websettings_app_factory(config, core):
    from mopidy.http.handlers import StaticFileHandler
    path = os.path.join(os.path.dirname(__file__), 'js')
    return [
        ('/',        WebSettingsRequestHandler, {'config': config}),
        ('/save',    WebPostRequestHandler,     {'config': config}),
        ('/apply',   WebApplyRequestHandler,),
        ('/reboot',  WebRebootRequestHandler,),
        ('/shutdown', WebShutdownRequestHandler,),
        (r'/js/(.*)', StaticFileHandler, {'path': path})
    ]
