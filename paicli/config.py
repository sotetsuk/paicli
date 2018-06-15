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
    _accesstoken = "access_token"

    # paths
    path_to_configdir = os.path.join(os.environ['HOME'], _paicli_dirname)
    path_to_configfile = os.path.join(os.environ['HOME'], _paicli_dirname, _configfile)
    path_to_accesstoken = os.path.join(os.environ['HOME'], _paicli_dirname, _accesstoken)

    def __init__(self, profile="default"):
        self.profile = profile
        self.host = "10.0.3.9"
        self._port = 'None'
        self._api_port = 9186
        self.username = "None"
        self.access_token = ""
        self.api_version = "v1"

    def add_profile(self):
        self.host = input("Host ip address for PAI [{}]: ".format(self.host)) or self.host
        self.port = input("Port for web portal [{}]: ".format(self.port)) or self.port
        self.api_port = input("Port for REST API [{}]: ".format(self.api_port)) or self.api_port
        self.username = input("Your username [{}]: ".format(self.username)) or self.username
        self.write_config()

    def load(self):
        with open(self.path_to_configfile) as f:
            yaml_config = ''.join(f.readlines())
            config = yaml.load(yaml_config)

        self.host = config[self.profile]["host"]
        self.port = config[self.profile]["port"]
        self.api_port = config[self.profile]["api_port"]
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
            "port": int(self._port),
            "api_port": int(self._api_port),
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
    def port(self, port):
        self._port = int(port)

    @property
    def api_port(self):
        return self._api_port

    @api_port.setter
    def api_port(self, api_port):
        self._api_port = int(api_port)

    @property
    def api_uri(self):
        return "http://{}:{}".format(self.host, self.api_port)