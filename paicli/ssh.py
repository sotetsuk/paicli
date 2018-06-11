"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import print_function

import os
import requests
import subprocess


def download_sshkey(content):
    res = requests.get(content['keyPair']['privateKeyDirectDownloadLink'])
    sshkey = res.content
    return sshkey


def run_ssh(config, content, sshkey, dryrun=False):
    path_to_sshkey = os.path.join(config.path_to_configdir, ".tmpkey")
    host = content["containers"][0]["sshIp"]
    port = content["containers"][0]["sshPort"]

    if os.path.exists(path_to_sshkey):
        os.remove(path_to_sshkey)

    with open(path_to_sshkey, 'w') as f:
        sshkey = sshkey.decode('utf-8')
        f.writelines(sshkey)
    os.chmod(path_to_sshkey, 0o600)

    cmd = ["ssh", "-i", path_to_sshkey, "-p", port, "root@{}".format(host)]

    if dryrun:
        print(' '.join(cmd))
    else:
        try:
            subprocess.call(cmd)
        finally:
            if os.path.exists(path_to_sshkey):
                os.remove(path_to_sshkey)
