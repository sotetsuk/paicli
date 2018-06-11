"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import print_function
import os
import sys
import json
import yaml
import getpass

from .api import API

if sys.version_info[0] == 2:
    input = raw_input


class Config(object):

    # consts
    _paicli_dirname = ".paicli"
    _configfile = "config.yaml"
    _accesstoken = "access_token"

    # paths
    path_to_configdir = os.path.join(os.environ['HOME'], _paicli_dirname)
    path_to_configfile = os.path.join(os.environ['HOME'], _paicli_dirname, _configfile)
    path_to_accesstoken = os.path.join(os.environ['HOME'], _paicli_dirname, _accesstoken)

    # configs
    host = "10.0.3.9"
    _port = 9286
    _api_port = 9186
    username = ""
    access_token = ""
    api_version = "v1"

    def __init__(self):
        pass

    def load(self):
        self.load_config()
        # self.load_access_token()

    def initialize(self):
        print("-" * 60)
        print("Initialize config file: '$HOME/.paicli/config.yaml'")
        print("-" * 60)
        self.host = input("2. host: [{}]\n".format(self.host)) or self.host
        self.port = input("3. port: port for web portal [{}]\n".format(self.port)) or self.port
        self.api_port = input("4. api_port: port for REST API [{}]\n".format(self.api_port)) or self.api_port
        self.username = input("1. username [{}]:\n".format(self.username)) or self.username
        self.write_config()

        # initialize token
        print("-" * 60)
        print("Initialize access token: '$HOME/.paicli/access_token'")
        print("-" * 60)
        api = API(self)
        ret = api.post_token(self.username, getpass.getpass("Enter password:\n"))
        self.access_token = json.loads(ret)['token']
        self.write_access_token()

    def load_config(self):
        with open(self.path_to_configfile) as f:
            yaml_config = ''.join(f.readlines())
            config = yaml.load(yaml_config)

        self.host = config["host"]
        self.port = config["port"]
        self.api_port = config["api_port"]
        self.username = config["username"]

    def load_access_token(self):
        if not os.path.exists(self.path_to_accesstoken):
            return

        with open(self.path_to_accesstoken, 'r') as f:
            self.access_token = f.readline().strip('\n').strip()

    def write_config(self):
        if not os.path.exists(self.path_to_configdir):
            os.makedirs(self.path_to_configdir)

        with open(self.path_to_configfile, 'w') as f:
            config_dic = {
                "host": str(self.host),
                "port": int(self._port),
                "api_port": int(self._api_port),
                "username": str(self.username),
            }
            f.writelines(yaml.dump(config_dic, default_flow_style=False))

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