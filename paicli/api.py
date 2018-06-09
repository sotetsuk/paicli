import json
import requests
from termcolor import colored

class API(object):

    """API client for PAI

    See: https://github.com/Microsoft/pai/blob/master/rest-server/README.md
    """

    def __init__(self, config):
        self.config = config

    def post_token(self, username, password, expiration=500000):
        url = "{}/api/{}/token".format(self.config.api_uri, self.config.api_version)
        headers = {"Content-type": "application/json"}
        data = json.dumps({
            "username": username,
            "password": password,
            "expiration": expiration
        })
        res = requests.post(url, headers=headers, data=data)

        if res.ok:
            return res.content
        else:
            res.raise_for_status()

    def put_user(self):
        pass

    def delete_user(self):
        """Admin only."""
        pass

    def put_user_username_virtualclusters(self):
        """Admin only."""
        pass

    def get_jobs(self, username=""):
        url = "{}/api/{}/jobs".format(self.config.api_uri, self.config.api_version)

        params = {} if not username else {"username": username}
        res = requests.get(url=url, params=params)

        if res.ok:
            return res.content
        else:
            print(res.raise_for_status())

    def get_jobs_jobname(self, jobname):
        pass

    def post_jobs(self, job_config_json):
        url = "{}/api/{}/jobs".format(self.config.api_uri, self.config.api_version)
        headers = {
            "Authorization": "Bearer {}".format(self.config.access_token),
            "Content-type": "application/json"
        }

        res = requests.post(url, headers=headers, data=job_config_json)

        if res.ok:
            return res.content
        elif res.status_code == 401:
            print(colored("Submission failed.", "red"))
            print("Access token seems to be expired.")
            print("Update your token by 'paicli token', then try again.\n")
            res.raise_for_status()
        elif res.status_code == 400:
            print(colored("Submission failed.", "red"))
            print("This may be caused by duplicated submission.\n")
            res.raise_for_status()
        else:
            print(colored("Submission failed.\n", "red"))
            res.raise_for_status()

    def get_jobs_jobname_config(self, jobname):
        pass

    def get_jobs_jobname_ssh(self, job_name):
        uri = "{}/api/{}/jobs/{}/ssh".format(self.config.api_uri, self.config.api_version, job_name)
        res = requests.get(uri)

        if res.ok:
            return res.content
        else:
            res.raise_for_status()

    def put_jobs_jobname_executiontype(self, jobname):
        pass

    def get_virtualclusters(self):
        pass

    def get_virtualclusters_vcname(self, vcname):
        pass