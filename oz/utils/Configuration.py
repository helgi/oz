import os
from os.path import expanduser, join
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import oz.ozutil
import oz.OzException


class Configuration:
    def parse(self, config_file):
        # if config_file was not None on input, then it was provided by the caller
        # and we use that instead
        if config_file is None:
            if os.geteuid() == 0:
                config_file = "/etc/oz/oz.cfg"
            else:
                config_file = "~/.oz/oz.cfg"

        config_file = expanduser(config_file)

        config = configparser.SafeConfigParser()
        if os.access(config_file, os.F_OK):
            config.read(config_file)

        return config

    def config_get_key(self, config, section, key, default):
        """
        Function to retrieve config parameters out of the config file.
        """
        if config is not None and config.has_section(section) and config.has_option(section, key):
            return config.get(section, key)
        else:
            return default

    def config_get_boolean_key(self, config, section, key, default):
        """
        Function to retrieve boolean config parameters out of the config file.
        """
        value = self.config_get_key(config, section, key, None)
        if value is None:
            return default

        retval = oz.ozutil.string_to_bool(value)
        if retval is None:
            raise Exception("Configuration parameter '%s' must be True, Yes, False, or No" % (key))

        return retval

    def defaults(self):
        if os.geteuid() == 0:
            output_dir = "/var/lib/libvirt/images"
            data_dir = "/var/lib/oz"
        else:
            output_dir = "~/.oz/images"
            data_dir = "~/.oz"

        defaults = {
            'paths': {
                'output_dir': expanduser(output_dir),
                'data_dir': expanduser(data_dir),
                'screenshot_dir': join(expanduser(data_dir), "screenshots")
            },
            'libvirt': {
                'uri': 'qemu:///system',
                'type': None,
                'bridge_name': None,
                'cpus': 1,
                'memory': 1024
            },
            'cache': {
                'original_media': True,
                'modified_media': False,
                'jeos': False
            },
        }