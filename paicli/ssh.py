"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import print_function

import os
import requests
import subprocess
import codecs
import json
from .utils import to_str
from .intereactive import select_choices_interactively


def run_ssh(api, jobname, config, content, dryrun=False):
    sshkey = _download_sshkey(content)
    path_to_sshkey = os.path.join(config.path_to_configdir, ".tmpkey")

    host = ""
    port = -1
    if len(content["containers"]) == 1:
        host = content["containers"][0]["sshIp"]
        port = content["containers"][0]["sshPort"]
    else:
        choices = []
        ret = api.get_jobs_jobname(jobname) # TODO: Error handling
        tasks = json.loads(ret)['taskRoles']
        for k, v in tasks.items():
            task_name = k
            tasks_statuses = v['taskStatuses']
            for task_status in tasks_statuses:
                task_index = task_status['taskIndex']
                container_id = task_status['containerId']
                container_ip = task_status['containerIp']
                choices.append(
                    (to_str("{} [{}] {}".format(task_name, task_index, container_ip)), container_id)
                )

        selected = select_choices_interactively([c[0] for c in choices])
        _id = dict(choices)[selected]
        for c in content["containers"]:
            if c["id"] == _id:
                host = c["sshIp"]
                port = c["sshPort"]
                break

    if os.path.exists(path_to_sshkey):
        os.remove(path_to_sshkey)

    with codecs.open(path_to_sshkey, 'w', 'utf-8') as f:
        f.writelines(sshkey)
    os.chmod(path_to_sshkey, 0o600)

    cmd = ["ssh", "-i", path_to_sshkey, "-p", port, "-oStrictHostKeyChecking=no", "root@{}".format(host)]

    if dryrun:
        print(' '.join(cmd))
    else:
        try:
            subprocess.call(cmd)
        finally:
            if os.path.exists(path_to_sshkey):
                os.remove(path_to_sshkey)


def _download_sshkey(content):
    res = requests.get(content['keyPair']['privateKeyDirectDownloadLink'])
    sshkey = res.content
    return to_str(sshkey)
