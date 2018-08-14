import json
import getpass

from .utils import to_str


def token(api, expiration):
    password = ""
    if api.config.password:
        password = api.config.password
    else:
        password = to_str(getpass.getpass("Enter password:\n"))
    ret = api.post_token(api.config.username, password, expiration)
    token = json.loads(ret)['token']
    api.config.access_token = token
    api.config.write_access_token()
