"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import print_function
import sys
import click
import logging
import json
from termcolor import colored
import requests
from prettytable import PrettyTable

from .config import Config
from .jobs import Jobs
from .ssh import run_ssh
from .intereactive import select_choices_interactively
from .api import API
from .cmd import token


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

if sys.platform.lower()[:3] == "win":
    import colorama
    colorama.init()


def _load(config):
    try:
        config.load()
    except FileNotFoundError as e:
        print("Config file does not exist. Run 'pai config'")
        exit(1)


@click.group(help="A CLI tool for PAI (Platform for AI).")
def main():
    pass


@click.command('config', help="Add a your configuration in $HOME/.paicli")
@click.option('--profile', '-p', type=str, default='default', help="Add another profile configuration.")
def configcmd(profile):
    config = Config(profile)
    try:
        config.load()
    except FileNotFoundError as e:
        pass  # No config file
    except KeyError as e:
        pass  # No same profile

    config.add_profile()  # Anyway, add new profile or modify the profile


@click.command('token', help="Update access token.")
@click.option('--expiration', '-e', type=int, default=500000, help="Expiration time.")
@click.option('--profile', '-p', type=str, default='default', help="Use a specified profile.")
def tokencmd(expiration, profile):
    config = Config(profile)
    _load(config)
    api = API(config)

    try:
        token(api, expiration)
    except requests.HTTPError as e:
        print(colored("Failed to update access token.\n", "red"))
        print(e)
        exit(1)


@click.command(name='ssh', help="SSH into a running container in PAI.")
@click.argument('jobname', type=str, default='')
@click.option('--task-name', '-t', type=str, default='')
@click.option('--task-index', '-i', type=int, default=-1)
@click.option('--username', '-u', type=str, default='')
@click.option('--command', '-c', type=str, default='')
@click.option('--dryrun', '-d', is_flag=True)
@click.option('--profile', '-p', type=str, default='default', help="Use a specified profile.")
def sshcmd(jobname, task_name, task_index, username, command, dryrun, profile):
    config = Config(profile)
    _load(config)
    api = API(config)

    if not jobname:
        if not username:
            username = config.username
        jobs = Jobs(api, username)
        jobs.filter({'state': ['RUNNING']})
        if len(jobs) == 0:
            print("There is no running jobs.")
            exit(1)
        choices = [job['name'] for job in jobs]
        _jobname = select_choices_interactively(choices)
    else:
        _jobname = jobname

    content = None
    try:
        content = json.loads(api.get_user_username_jobs_jobname_ssh(username, _jobname))
    except requests.HTTPError as e:
        # This method is duplicated in the latest API
        # So this nested try-catch should be removed in the near future
        try:
            content = json.loads(api.get_user_username_jobs_jobname_ssh(config.username, _jobname))
        except requests.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                print(colored("SSH failed.", "red"))
                if jobname:
                    print("Wrong job name or SSH is not ready yet.\n")
                else:
                    print("SSH is not ready yet. Wait a minute and try again.\n")
            print(e)
            exit(1)

    try:
        run_ssh(api, _jobname, task_name, task_index, config, content, command, dryrun)
    except KeyError:  # TODO: raise/catch original error
        print(colored("SSH failed.", "red"))
        print("There is no match task.\n")  # TODO: give more information
        exit(1)


@click.command(name='jobs', help="Show jobs in PAI.")
@click.option('--username', '-u', multiple=True)
@click.option('--state', '-s', multiple=True)
@click.option('--num-jobs', '-n', type=int, default=20)
@click.option('--profile', '-p', type=str, default='default', help="Use a specified profile.")
def jobscmd(username, state, num_jobs, profile):
    config = Config(profile)
    _load(config)
    api = API(config)

    jobs = Jobs(api)
    filter_dic = {}
    if len(username) != 0:
        filter_dic['username'] = username
    if len(state) != 0:
        filter_dic['state'] = state
    if filter_dic:
        jobs.filter(filter_dic)
    jobs.show(num_jobs)


@click.command(name='submit',
               help="Submit your job into PAI. With no json files, or when '-' is specified, read standard input.")
@click.argument('job_config_json', nargs=-1, required=False)
@click.option('--profile', '-p', type=str, default='default', help="Use a specified profile.")
def submitcmd(job_config_json, profile):
    config = Config(profile)
    _load(config)
    api = API(config)

    job_config_json_list = []
    if job_config_json and job_config_json[0] != '-':
        for _job_config_json in job_config_json:
            with open(_job_config_json, 'r') as f:
                job_config_json_list.append(''.join([line.strip('\n').strip() for line in f.readlines()]))
    else:
        stdin_json = ""
        for line in sys.stdin:
            stdin_json += line.strip('\n').strip()
        job_config_json_list.append(stdin_json)

    for _job_config_json in job_config_json_list:
        try:
            api.post_user_username_jobs(config.username, _job_config_json)
            print(colored("Successfully submitted!", "green") + ": {}"
                  .format(json.loads(_job_config_json)['jobName']))
        except requests.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                print(colored("Submission failed.", "red"))
                print("Access token seems to be expired.")
                print("Update your token by 'pai token', then try again.\n")
            elif status_code == 400:
                print(colored("Submission failed.", "red"))
                print("This may be caused by duplicated submission.\n")
            else:
                print(colored("Submission failed.\n", "red"))
            print(e)
            exit(1)
        except requests.Timeout as e:
            print(colored("Submission failed.\n", "red"))
            print(e)
            exit(1)
        except requests.ConnectionError as e:
            print(colored("Submission failed.\n", "red"))
            print(e)
            exit(1)
        except requests.RequestException as e:
            print(colored("Submission failed.\n", "red"))
            print(e)
            exit(1)
        except FileNotFoundError as e:
            print(colored("Submission failed.\n", "red"))
            print("Access token does not exist. Run 'pai token'")
            exit(1)


@click.command(name='stop', help="Stop a job in PAI.")
@click.argument('jobname', type=str, nargs=-1)
@click.option('--profile', '-p', type=str, default='default', help="Use a specified profile.")
def stopcmd(jobname, profile):
    config = Config(profile)
    _load(config)
    api = API(config)

    if not jobname:
        jobs = Jobs(api, config.username)
        jobs.filter({'state': ['RUNNING']})
        choices = [job['name'] for job in jobs]
        jobname = (select_choices_interactively(choices), )

    for _jobname in jobname:
        try:
            api.put_user_username_jobs_jobname_executiontype(config.username, _jobname, "STOP")
            print(colored("Stop signal submitted!", "green") + ": {}".format(_jobname))
        except requests.HTTPError as e:
            print(colored("Failed to submit a stop signal.\n", "red"))
            print(e)
            exit(1)
        except requests.Timeout as e:
            print(colored("Failed to submit a stop signal.\n", "red"))
            print(e)
            exit(1)
        except requests.ConnectionError as e:
            print(colored("Failed to submit a stop signal.\n", "red"))
            print(e)
            exit(1)
        except requests.RequestException as e:
            print(colored("Failed to submit a stop signal.\n", "red"))
            print(e)
            exit(1)
        except FileNotFoundError:
            print(colored("Failed to submit a stop signal.\n", "red"))
            print("Access token does not exist. Run 'pai token'")
            exit(1)


@click.command(name='host', help="Show host information of a job.")
@click.argument('jobname', type=str)
@click.option('--profile', '-p', type=str, default='default', help="Use a specified profile.")
def hostcmd(jobname, profile):
    config = Config(profile)
    _load(config)
    api = API(config)

    tab = PrettyTable()
    tab.field_names = ["task role", "ip", "port label", "port"]

    try:
        ret = api.get_jobs_jobname(jobname)
        tasks = json.loads(ret)['taskRoles']
        for k, v in tasks.items():
            task_name = k
            tasks_statuses = v['taskStatuses']
            for task_status in tasks_statuses:
                container_ip = task_status['containerIp']
                container_ports = task_status['containerPorts']
                for port_label, port in container_ports.items():
                    tab.add_row([task_name, container_ip, port_label, port])

        tab.border = False
        print(tab.get_string())

    except requests.HTTPError as e:
        print(colored("Failed to get a host information.\n", "red"))
        print(e)
        exit(1)
    except requests.Timeout as e:
        print(colored("Failed to get a host information.\n", "red"))
        print(e)
        exit(1)
    except requests.ConnectionError as e:
        print(colored("Failed to get a host information.\n", "red"))
        print(e)
        exit(1)
    except requests.RequestException as e:
        print(colored("Failed to get a host information.\n", "red"))
        print(e)
        exit(1)


main.add_command(configcmd)
main.add_command(tokencmd)
main.add_command(sshcmd)
main.add_command(jobscmd)
main.add_command(submitcmd)
main.add_command(stopcmd)
main.add_command(hostcmd)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(module)s.%(funcName)s %(levelname)s \t: %(message)s')
    logging.debug("Program start.")
    main()
