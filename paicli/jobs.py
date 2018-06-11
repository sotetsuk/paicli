"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import division
from datetime import datetime
import json
from prettytable import PrettyTable
from termcolor import colored


class Jobs(object):

    def __init__(self, api, username=""):

        self._api = api
        self._jobs = json.loads(self._api.get_jobs(username))
        for job in self._jobs:
            job["createdTime"] = datetime.fromtimestamp(int(job["createdTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    def __getitem__(self, item):
        return self._jobs[item]

    def __len__(self):
        return len(self._jobs)

    def filter(self, dic):
        """Filter jobs

        EXAMPLE
        -------
        >>> jobs = Jobs(api)
        >>> jobs.filter({"state", ["RUNNING", "SUCCEEDED"]})

        :param dic: dictionary of (str, list)
        """
        _content = []
        for job in self._jobs:
            for key, val in dic.items():
                if job[key] not in val:
                    break
            else:
                _content.append(job)

        self._jobs = _content

    def show(self, n=None):
        tab = PrettyTable()
        tab.field_names = ["name", "username", "virtual cluster", "created time", "retries", "state"]
        for i, line in enumerate(self):
            state = line["state"]
            if state == "SUCCEEDED":
                state = colored(state, "green")
            elif state == "RUNNING":
                state = colored(state, "cyan")
            elif state == "FAILED":
                state = colored(state, "red")

            tab.add_row([line["name"], line["username"], line["virtualCluster"],
                         line["createdTime"], line["retries"], state])

            if n is not None and i + 1 >= n:
                break

        tab.border = False
        print(tab.get_string())

