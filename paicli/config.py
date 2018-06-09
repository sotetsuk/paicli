from __future__ import print_function
import os
import yaml


class Config(object):

    def __init__(self):
        self._paicli_dirname = ".paicli"
        self.host = "10.0.3.9"
        self._port = 9286
        self._api_port = 9186
        self.username = ""
        self.password = ""  # TODO: fix to use stdin like docker-cli

        # consts
        self._configfile = "config.yaml"

        self.path_to_configdir = os.path.join(os.environ['HOME'], self.paicli_dirname)
        self.path_to_configfile = os.path.join(os.environ['HOME'],
                                               self.paicli_dirname, self._configfile)

    def load_config(self):
        if not self.path_to_configdir:
            return

        try:
            with open(self.path_to_configfile) as f:
                yaml_config = ''.join(f.readlines())
                config = yaml.load(yaml_config)
        except Exception as e:
            print("Failed to load config file from '{}':\n  {}".format(self.path_to_configfile, e))
            return

        self.host = config["host"]
        self.port = config["port"]
        self.api_port = config["api_port"]
        self.username = config["username"]
        self.password = config["password"]

    def write_config(self):
        if not self.path_to_configdir:
            os.makedirs(self.path_to_configdir)

        with open(self.path_to_configfile, 'w') as f:
            config_dic = {
                "host": str(self.host),
                "port": int(self._port),
                "api_port": int(self._api_port),
                "username": str(self.username),
                "password": str(self.password)
            }
            f.writelines(yaml.dump(config_dic, default_flow_style=False))

    @property
    def paicli_dirname(self):
        return self._paicli_dirname

    @paicli_dirname.setter
    def paicli_dirname(self, paicli_dirname):
        self._paicli_dirname = paicli_dirname
        self.path_to_configdir = os.path.join(os.environ['HOME'], self.paicli_dirname)
        self.path_to_configfile = os.path.join(os.environ['HOME'],
                                               self.paicli_dirname, self._configfile)

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


class APIInfo(object):

    def __init__(self, config):
        self.url = config.host
        self.port = config.api_port
        self.version = "v1"

        self.uri = "http://{}:{}".format(self.url, self.port)
