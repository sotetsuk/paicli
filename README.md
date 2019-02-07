[![PyPI version](https://badge.fury.io/py/paicli.svg)](https://badge.fury.io/py/paicli)
![Python version](https://img.shields.io/pypi/pyversions/paicli.svg?style=flat)
[![License MIT](https://img.shields.io/github/license/sotetsuk/paicli.svg)](https://github.com/sotetsuk/paicli/blob/master/LICENSE)

# paicli

A CLI tool for [OpenPAI](https://github.com/microsoft/pai), which supports basic opperations like listing up jobs, submitting a new job, suspending a running job, and executing ssh into a running container.

[![demo](https://raw.githubusercontent.com/sotetsuk/paicli/master/demo.gif)](https://asciinema.org/a/225718)

## How to install
One can install paicli from [PyPI](https://pypi.org/project/paicli/).

```
$ pip install paicli
```

## Basic usage
For more detailed usage, one can use `--help` option for each subcommand like `pai config --help`.

```
$ pai --help
Usage: pai [OPTIONS] COMMAND [ARGS]...

  A CLI tool for OpenPAI.

Options:
  --help  Show this message and exit.

Commands:
  config  Write your configuration to a file.
  host    Show host information of the specified job.
  jobs    Show job list.
  ssh     SSH into a running container.
  stop    Stop a running job.
  submit  Submit your job.
  token   Generate a new access token
```

## Configuration

- **Config file**: To initialize your config file, run `pai config`. Then your config file will be located in `$HOME/.paicli`. You should set your `host`, `port`, and `username`.
- **Access token**: Before submitting/stopping a job, you should issue your access token by executing `pai token` and entering your password. You can skip entering password everytime if you write your password directly to your config file (not recommended).

## Practical examples
One can utilize and combine the paicli subcommands to achieve several practical operations.

### 1. Submit multiple jobs with one line

Use `pai submit` and some template engine like [envsubst](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html).

```sh
$ head template.json -n 2
{
  "jobName": "template-${JOBID}"
$ for i in `seq 1 3`; do cat template.json | JOBID=$i envsubst | pai submit; done
```

### 2. Stop multiple jobs with one line

Combine `pai jobs` and `pai stop`.

```sh
$ pai jobs -u sotetsuk -s RUNNING | grep template | awk '{print $1}' | xargs pai stop
```

### 3. Ssh into multiple running containers and run the same command

Combine `pai jobs` and `pai ssh`. In this example, show python processes in multiple jobs with one line.

```sh
$ pai jobs -u sotetsuk -s RUNNING | grep template | awk '{print $1}' | xargs -n 1 pai ssh -c "ps -aux | grep python"
```

### 4. Show all tensorboard URLs in running jobs

Combine `pai jobs` and `pai host` to show all tensorboard URLs. One can use some browser extention to open all URLs (e.g., [OpenList](https://chrome.google.com/webstore/detail/openlist/nkpjembldfckmdchbdiclhfedcngbgnl?hl=en))

```sh
$ pai jobs -u sotetsuk -s RUNNING | grep template | xargs -n 1 pai host | grep tensorboard | awk '{printf "http://%s:%s\n",$2,$4}'
http://10.0.0.1:9999
http://10.0.0.2:9999
http://10.0.0.3:9999
```

## Author
Sotetsu KOYAMADA
