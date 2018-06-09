import requests


class API(object):

    """API client for PAI

    See: https://github.com/Microsoft/pai/blob/master/rest-server/README.md
    """

    def __init__(self, config):
        self.config = config

    def post_token(self):
        pass

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

    def post_jobs(self):
        pass

    def get_jobs_jobname_config(self, jobname):
        pass

    def get_jobs_jobname_ssh(self, job_name):
        uri = "{}/api/{}/jobs/{}/ssh".format(self.config.api_uri, self.config.api_version, job_name)
        res = requests.get(uri)

        if res.ok:
            return res.content
        else:
            print(res.raise_for_status())

    def put_jobs_jobname_executiontype(self, jobname):
        pass

    def get_virtualclusters(self):
        pass

    def get_virtualclusters_vcname(self, vcname):
        pass