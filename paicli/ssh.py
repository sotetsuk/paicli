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


def run_ssh(api, username, jobname, task_name, task_index, config, content, command="", dryrun=False):
    sshkey = _download_sshkey(content)
    path_to_sshkey = os.path.join(config.path_to_configdir, ".tmpkey")

    host = ""
    port = -1

    # if the job has only one task
    if len(content["containers"]) == 1:
        host = content["containers"][0]["sshIp"]
        port = content["containers"][0]["sshPort"]
    # if the job has >= 2 tasks
    else:
        choices = []
        ret = api.get_user_username_jobs_jobname(username, jobname) # TODO: Error handling
        tasks = json.loads(ret)['taskRoles']
        for k, v in tasks.items():
            _task_name = k
            if task_name and _task_name != task_name:
                continue
            tasks_statuses = v['taskStatuses']
            for task_status in tasks_statuses:
                _task_index = task_status['taskIndex']
                if task_index != -1 and task_index != _task_index:
                    continue
                container_id = task_status['containerId']
                container_ip = task_status['containerIp']
                choices.append(
                    (to_str("{} [{}] {}".format(_task_name, _task_index, container_ip)), container_id)
                )

        if not choices:
            raise KeyError  # TODO: raise original Error (No such job/task/task_index)

        if len(choices) == 1:
            _id = choices[0][1]
        else:
            selected = select_choices_interactively([c[0] for c in choices])
            _id = dict(choices)[selected]

        # select unique host/port from given container id
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
    if command:
        cmd.append(command)

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
