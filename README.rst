****************************
Mopidy-WebSettings
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-WebSettings.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-WebSettings/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Mopidy-WebSettings.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-WebSettings/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/pimusicbox/mopidy-websettings/develop.svg?style=flat
    :target: https://travis-ci.org/pimusicbox/mopidy-websettings
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/pimusicbox/mopidy-websettings/develop.svg?style=flat
   :target: https://coveralls.io/r/pimusicbox/mopidy-websettings?branch=develop
   :alt: Test coverage

Mopidy extension for editing settings in a webinterface. Used by Pi MusicBox, but also usable for personal installations or other projects, since MusicBox-only settings are hidden automatically.


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

- `Source code <https://github.com/pimusicbox/mopidy-websettings>`_
- `Issue tracker <https://github.com/pimusicbox/mopidy-websettings/issues>`_
- `Development branch tarball <https://github.com/pimusicbox/mopidy-websettings/archive/develop.tar.gz#egg=Mopidy-WebSettings-dev>`_


Changelog
=========

v0.1.6 (18/3/2016)
--------------------

- Updated and improved explanations for settings.
- Removed development-orientated resize_once option.
- Fixed corrupt settings when expected subsections missing from settings.ini.
- Fixed webclient not changing.
- Changing the webclient requires a Mopidy restart rather than a reboot.
- Fixed outdated Exception syntax.
- Option to populate autoplay with currently playing track. 

v0.1.5 (2/3/2016)
--------------------

- Fixed password field length restrictions.
- Apply changes with Mopidy service restart rather than system reboot where possible.
- Added/updated options as required for integration with PiMusicbox v0.7.

v0.1.4.2 (26/3/2015)
--------------------

- Fixed length of Autoplay URL input box.

v0.1.4.1
----------------------------------------

- Small fix for passwords not updated well

v0.1.4
----------------------------------------

- AudioAddict added (by Nilicule)
- Passwords mask same size as password

v0.1.3 
----------------------------------------

- Added YouTube and local support (on or off)
- Enabled YouTube, SomaFM, Local, Internetarchive, Podcast by default when not in ini-file (the default of the extensions)
- Settings for enabling streaming services shairport and upmpdcli (for MusicBox only)
- Writing the config is more reliable
- Better layout

v0.1.2
----------------------------------------

- Fixes for writing ini file


v0.1.1 
----------------------------------------

- Fixed missing template files in dist
- Fixed template
- Reboot after settings are updated (if mopidy instance has the permission to do that, like on musicbox)

v0.1.0 
----------------------------------------

- Initial release
