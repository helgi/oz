# -*- coding: utf-8 -*-
# Copyright (C) 2012  Helgi Þorbjörnsson <helgi@php.net>
import os
from os.path import expanduser, join
from simpleconfigparser import simpleconfigparser


class Configuration:
    """
    Manages the Oz configuration and owns the defaults for oz.cfg
    """
    def parse(self, config_file=None):
        if config_file is None:
            if os.geteuid() == 0:
                config_file = "/etc/oz/oz.cfg"
            else:
                config_file = expanduser("~/.oz/oz.cfg")

        config = simpleconfigparser(defaults=self.gather_defaults())
        if os.access(config_file, os.F_OK):
            config.read(config_file)

        return config

    def gather_defaults(self):
        if os.geteuid() == 0:
            data_dir = "/var/lib/oz"
            output_dir = "/var/lib/libvirt/images"
        else:
            data_dir = expanduser("~/.oz")
            output_dir = join(data_dir, "images")

        defaults = {
            'paths': {
                'output_dir': output_dir,
                'data_dir': data_dir,
                'screenshot_dir': join(data_dir, 'screenshots')
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

        return defaults
