from __future__ import print_function

import sys
import click
import json
import getpass

from .config import Config, APIInfo
from .jobs import Jobs
from .ssh import download_sshkey, run_ssh
from .intereactive import select_job_interactively
from .api import API

if sys.version_info[0] == 2:
    input = raw_input

config = Config()
config.load_config()
api_info = APIInfo(config)
api = API(api_info)


@click.group()
def main():
    pass


@click.command("token", help="Update access token.")
@click.option('--expiration' '-e', type=int, help="Expiration time ")
def tokencmd():
    ret = api.post_token(config.username, getpass.getpass("Enter password:\n"), 60)
    print(json.loads(ret)['token'])


@click.command(name="ssh")
@click.option('--jobname', '-j', type=str, default="")
def sshcmd(jobname):
    if not jobname:
        jobs = Jobs(api, config.username)
        jobs.filter({'state': ['RUNNING']})
        jobname = select_job_interactively(jobs)

    content = json.loads(api.get_jobs_jobname_ssh(jobname))
    sshkey = download_sshkey(content)
    run_ssh(config, content, sshkey)


@click.command(name="jobs")
@click.option('--username', '-u', multiple=True)
@click.option('--state', '-s', multiple=True)
@click.option('-n', type=int, default=20)
def jobscmd(username, state, n):
    jobs = Jobs(api)
    filter_dic = {}
    if len(username) != 0:
        filter_dic['username'] = username
    if len(state) != 0:
        filter_dic['state'] = state
    if filter_dic:
        jobs.filter(filter_dic)
    jobs.show(n)


main.add_command(tokencmd)
main.add_command(sshcmd)
main.add_command(jobscmd)

if __name__ == '__main__':
    main()