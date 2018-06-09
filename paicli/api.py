import json
import requests


class API(object):

    """API client for PAI

    See: https://github.com/Microsoft/pai/blob/master/rest-server/README.md
    """

    def __init__(self, api_info):
        self.api_info = api_info

    def get_jobs(self, username=""):
        url = "{}/api/{}/jobs".format(self.api_info.uri, self.api_info.version)

        params = {} if not username else {"username": username}
        res = requests.get(url=url, params=params)

        if res.ok:
            return json.loads(res.content)
        else:
            print(res.raise_for_status())

    def get_jobs_jobname_ssh(self, job_name):
        uri = "{}/api/{}/jobs/{}/ssh".format(self.api_info.uri, self.api_info.version, job_name)
        res = requests.get(uri)

        if res.ok:
            return json.loads(res.content)
        else:
            print(res.raise_for_status())


