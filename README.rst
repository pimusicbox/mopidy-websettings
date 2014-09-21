****************************
Mopidy-WebSettings
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-WebSettings.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-WebSettings/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Mopidy-WebSettings.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-WebSettings/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/woutervanwijk/mopidy-websettings/master.png?style=flat
    :target: https://travis-ci.org/woutervanwijk/mopidy-websettings
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/woutervanwijk/mopidy-websettings/master.svg?style=flat
   :target: https://coveralls.io/r/woutervanwijk/mopidy-websettings?branch=master
   :alt: Test coverage

Mopidy extension for editing settings in a webinterface. Used by Pi MusicBox


Installation
============

Install by running::

    pip install Mopidy-WebSettings

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you can add configuration for
Mopidy-WebSettings to your Mopidy configuration file::

    [websettings]
    enabled = true
    musicbox = false
    config_file = /etc/mopidy/mopidy.conf

Make sure the config file is writable by the user under which mopidy is running! And make sure the http extension is working. Go to the ip or url of your mopidy computer and add /settings (e.g. http://musicbox.local/settings or http://192.168.1.10:6680/settings )

For now, the settings are only applied after a reboot, which this extension will try to do. If it doesn't work, a (manual) restart of mopidy is needed. 

Project resources
=================

- `Source code <https://github.com/woutervanwijk/mopidy-websettings>`_
- `Issue tracker <https://github.com/woutervanwijk/mopidy-websettings/issues>`_
- `Development branch tarball <https://github.com/woutervanwijk/mopidy-websettings/archive/master.tar.gz#egg=Mopidy-WebSettings-dev>`_


Changelog
=========

v0.1.1 
----------------------------------------

- Fixed missing template files in dist
- Fixed template
- Reboot after settings are updated (if mopidy instance has the permission to do that, like on musicbox)

v0.1.0 
----------------------------------------

- Initial release