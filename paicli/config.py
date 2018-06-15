"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import print_function
import os
import sys
import yaml

if sys.version_info[0] == 2:
    input = raw_input

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class Config(object):

    # consts
    _paicli_dirname = ".paicli"
    _configfile = "config.yaml"
    _accesstoken = ".token_{}"

    # paths
    path_to_configdir = os.path.join(os.environ['HOME'], _paicli_dirname)
    path_to_configfile = os.path.join(os.environ['HOME'], _paicli_dirname, _configfile)

    def __init__(self, profile="default"):
        self.profile = profile
        self.host = "10.0.3.9"  # default
        self._port = 9186  # default
        self.username = "None"  # default
        self.access_token = ""
        self.api_version = "v1"

        self.path_to_accesstoken = os.path.join(os.environ['HOME'],
                                                self._paicli_dirname, self._accesstoken.format(self.profile))

    def add_profile(self):
        self.host = input("Host ip address for PAI [{}]: ".format(self.host)) or self.host
        self.port = input("Port for REST API [{}]: ".format(self.port)) or self.port
        self.username = input("Your username [{}]: ".format(self.username)) or self.username
        self.write_config()

    def load(self):
        with open(self.path_to_configfile) as f:
            yaml_config = ''.join(f.readlines())
            config = yaml.load(yaml_config)

        self.host = config[self.profile]["host"]
        self.port = config[self.profile]["port"]
        self.port = config[self.profile]["port"]
        self.username = config[self.profile]["username"]

    def load_access_token(self):
        with open(self.path_to_accesstoken, 'r') as f:
            self.access_token = f.readline().strip('\n').strip()

    def write_config(self):
        if not os.path.exists(self.path_to_configdir):
            os.makedirs(self.path_to_configdir)

        profiles = {}
        new_config = {
            "host": str(self.host),
            "port": int(self.port),
            "username": str(self.username),
        }
        try:
            with open(self.path_to_configfile, 'r') as f:
                profiles = yaml.load(''.join(f.readlines()))
                profiles[str(self.profile)] = new_config
        except FileNotFoundError:
            profiles[str(self.profile)] = new_config

        with open(self.path_to_configfile, 'w') as f:
            f.writelines(yaml.dump(profiles, default_flow_style=False))

    def write_access_token(self):
        if not os.path.exists(self.path_to_configdir):
            os.makedirs(self.path_to_configdir)

        with open(self.path_to_accesstoken, 'w') as f:
            f.write(self.access_token)

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, _port):
        self._port = int(_port)

    @property
    def api_uri(self):
        return "http://{}:{}".format(self.host, self.port)