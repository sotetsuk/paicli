"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import print_function

import click
import json
import getpass
from termcolor import colored
import requests

from .config import Config
from .jobs import Jobs
from .ssh import download_sshkey, run_ssh
from .intereactive import select_job_interactively
from .api import API

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


config = Config()


def load_config():
    try:
        config.load()
    except FileNotFoundError as e:
        print("Config file does not exist. Run 'paicli config'")
        exit(1)


@click.group(help="A CLI tool for PAI (Platform for AI).")
def main():
    pass


@click.command("config", help="Initialize your config information in $HOME/.paicli")
def configcmd():
    load_config()
    config.initialize()


@click.command("token", help="Update access token.")
@click.option('--expiration', '-e', type=int, default=500000, help="Expiration time.")
def tokencmd(expiration):
    load_config()
    api = API(config)

    ret = api.post_token(config.username, getpass.getpass("Enter password:\n"), expiration)
    token = json.loads(ret)['token']
    config.access_token = token
    config.write_access_token()


@click.command(name="ssh", help="SSH into a running container in PAI.")
@click.option('--jobname', '-j', type=str, default="")
def sshcmd(jobname):
    load_config()
    api = API(config)

    if not jobname:
        jobs = Jobs(api, config.username)
        jobs.filter({'state': ['RUNNING']})
        jobname = select_job_interactively(jobs)

    content = json.loads(api.get_jobs_jobname_ssh(jobname))
    sshkey = download_sshkey(content)
    run_ssh(config, content, sshkey)


@click.command(name="jobs", help="Show jobs in PAI.")
@click.option('--username', '-u', multiple=True)
@click.option('--state', '-s', multiple=True)
@click.option('-n', type=int, default=20)
def jobscmd(username, state, n):
    load_config()
    api = API(config)

    jobs = Jobs(api)
    filter_dic = {}
    if len(username) != 0:
        filter_dic['username'] = username
    if len(state) != 0:
        filter_dic['state'] = state
    if filter_dic:
        jobs.filter(filter_dic)
    jobs.show(n)


@click.command(name="submit", help="Submit your job into PAI.")
@click.argument('job_config_json')
def submitcmd(job_config_json):
    load_config()
    api = API(config)

    with open(job_config_json, 'r') as f:
        job_config_json = ''.join([line.strip('\n').strip() for line in f.readlines()])

    try:
        api.post_jobs(job_config_json)
        print(colored("Successfully submitted!", "green") + ": {}"
              .format(json.loads(job_config_json)['jobName']))
    except requests.HTTPError as e:
        status_code = str(e).split()[0]
        if status_code == '401':
            print(colored("Submission failed.", "red"))
            print("Access token seems to be expired.")
            print("Update your token by 'paicli token', then try again.\n")
        elif status_code == '400':
            print(colored("Submission failed.", "red"))
            print("This may be caused by duplicated submission.\n")
        else:
            print(colored("Submission failed.\n", "red"))

        print(e)
        exit(1)
    except requests.Timeout as e:
        print(e)
        exit(1)
    except requests.ConnectionError as e:
        print(e)
        exit(1)
    except FileNotFoundError as e:
        print(e)
        print("Access token does not exist. Run 'paicli token'")
        exit(1)


@click.command(name="stop", help="Stop a job in PAI.")
@click.option('--jobname', '-j', type=str, default="")
def stopcmd(jobname):
    load_config()
    api = API(config)

    if not jobname:
        jobs = Jobs(api, config.username)
        jobs.filter({'state': ['RUNNING']})
        jobname = select_job_interactively(jobs)

    try:
        api.put_jobs_jobname_executiontype(jobname, "STOP")
        print(colored("Stop signal submitted!", "green") + ": {}".format(jobname))
    except requests.HTTPError as e:
        print(e)
    except requests.Timeout as e:
        print(e)
        exit(1)
    except requests.ConnectionError as e:
        print(e)
        exit(1)
    except FileNotFoundError:
        print("Access token does not exist. Run 'paicli token'")


main.add_command(configcmd)
main.add_command(tokencmd)
main.add_command(sshcmd)
main.add_command(jobscmd)
main.add_command(submitcmd)
main.add_command(stopcmd)


if __name__ == '__main__':
    main()