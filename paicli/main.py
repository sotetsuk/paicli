from __future__ import print_function

import click
import json
from termcolor import colored

from .config import Config
from .jobs import Jobs
from .ssh import download_sshkey, run_ssh
from .intereactive import select_job_interactively
from .api import API


config = Config()
api = API(config)

@click.group()
def main():
    pass


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


@click.command(name="submit")
@click.argument('job_config_json')
def submitcmd(job_config_json):
    with open(job_config_json, 'r') as f:
        job_config_json = ''.join([line.strip('\n').strip() for line in f.readlines()])
    results = api.post_jobs(job_config_json)
    if results:
        print(colored("Successfully submitted!", "green") + ": {}"
              .format(json.loads(job_config_json)['jobName']))


main.add_command(sshcmd)
main.add_command(jobscmd)
main.add_command(submitcmd)

if __name__ == '__main__':
    main()