# -*- coding: utf-8 -*-
# Copyright (C) 2013 Helgi Þorbjörnsson <helgi@php.net>

import command
from os.path import dirname


class cmd:
    @classmethod
    def ssh(cls, guestaddr, sshprivkey, c, timeout=10, tunnels=None, debug=None):
        """
        Function to execute a command on the guest using SSH and return the
        output.
        """
        # ServerAliveInterval protects against NAT firewall timeouts
        # on long-running commands with no output
        #
        # PasswordAuthentication=no prevents us from falling back to
        # keyboard-interactive password prompting
        #
        # -F /dev/null makes sure that we don't use the global or per-user
        # configuration files

        cmd = ["ssh", "-i", sshprivkey,
               "-F", "/dev/null",
               "-o", "ServerAliveInterval=30",
               "-o", "StrictHostKeyChecking=no",
               "-o", "ConnectTimeout=" + str(timeout),
               "-o", "UserKnownHostsFile=/dev/null",
               "-o", "PasswordAuthentication=no"]

        if tunnels:
            for host in tunnels:
                for port in tunnels[host]:
                    cmd.append("-R %s:%s:%s" % (tunnels[host][port], host, port))

        cmd.extend(["root@" + guestaddr, c])

        return command.run(cmd, debug=debug)

    @classmethod
    def scp(cls, guestaddr, sshprivkey, file_to_upload, destination, timeout=10, debug=None):
        """
        Function to upload a file to the guest using scp.
        """
        cls.ssh(guestaddr, sshprivkey, "mkdir -p " + dirname(destination), timeout, debug=debug)

        # ServerAliveInterval protects against NAT firewall timeouts
        # on long-running commands with no output
        #
        # PasswordAuthentication=no prevents us from falling back to
        # keyboard-interactive password prompting
        #
        # -F /dev/null makes sure that we don't use the global or per-user
        # configuration files
        return command.run(["scp", "-i", sshprivkey,
                            "-F", "/dev/null",
                            "-o", "ServerAliveInterval=30",
                            "-o", "StrictHostKeyChecking=no",
                            "-o", "ConnectTimeout=" + str(timeout),
                            "-o", "UserKnownHostsFile=/dev/null",
                            "-o", "PasswordAuthentication=no",
                            file_to_upload,
                            "root@" + guestaddr + ":" + destination], debug=debug)
