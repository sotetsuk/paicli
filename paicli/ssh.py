from __future__ import print_function

import os
import requests
import subprocess


def download_sshkey(content):
    res = requests.get(content['keyPair']['privateKeyDirectDownloadLink'])
    if res.ok:
        sshkey = res.content
        return sshkey
    else:
        res.raise_for_status()


def run_ssh(config, content, sshkey):
    path_to_sshkey = os.path.join(config.path_to_configdir, ".tmpkey")
    host = content["containers"][0]["sshIp"]
    port = content["containers"][0]["sshPort"]

    if os.path.exists(path_to_sshkey):
        os.remove(path_to_sshkey)

    try:
        with open(path_to_sshkey, 'w') as f:
            f.writelines(sshkey)
        os.chmod(path_to_sshkey, 0o600)
    except Exception as e:
        raise e

    cmd = ["ssh", "-i", path_to_sshkey, "-p", port, "root@{}".format(host)]
    try:
        subprocess.call(cmd)
    finally:
        if os.path.exists(path_to_sshkey):
            os.remove(path_to_sshkey)
