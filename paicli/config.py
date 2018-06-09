from __future__ import print_function
import os
import yaml


class Config(object):

    def __init__(self):
        # consts
        self._paicli_dirname = ".paicli"
        self._configfile = "config.yaml"
        self._accesstoken = "access_token"

        # paths
        self.path_to_configdir = os.path.join(os.environ['HOME'], self._paicli_dirname)
        self.path_to_configfile = os.path.join(os.environ['HOME'],
                                               self._paicli_dirname, self._configfile)
        self.path_to_accesstoken = os.path.join(os.environ['HOME'],
                                                self._paicli_dirname, self._accesstoken)

        # configs
        self.host = "10.0.3.9"
        self._port = 9286
        self._api_port = 9186
        self.username = ""
        self.password = ""  # TODO: fix to use stdin like docker-cli
        self.access_token = None
        self.api_uri = "http://{}:{}".format(self.host, self.api_port)
        self.api_version = "v1"

        # load config files
        self.load_config()
        self.load_accesstoken()

    def load_config(self):
        if not os.path.exists(self.path_to_configdir):
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
        self.api_uri = "http://{}:{}".format(self.host, self.api_port)

    def load_accesstoken(self):
        if not os.path.exists(self.path_to_accesstoken):
            return

        with open(self.path_to_accesstoken, 'r') as f:
            self.access_token = f.readline().strip('\n').strip()

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

