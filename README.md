[![PyPI version](https://badge.fury.io/py/paicli.svg)](https://badge.fury.io/py/paicli)
[![License MIT](https://img.shields.io/github/license/sotetsuk/paicli.svg)](https://github.com/sotetsuk/paicli/blob/master/LICENSE)

# paicli
A CLI tool for [OpenPAI](https://github.com/microsoft/pai).

```
$ pai --help
Usage: pai [OPTIONS] COMMAND [ARGS]...

  A CLI tool for OpenPAI.

Options:
  --help  Show this message and exit.

Commands:
  config  Add a your configuration in $HOME/.paicli
  host    Show host information of a job.
  jobs    Show jobs in PAI.
  ssh     SSH into a running container in PAI.
  stop    Stop a job in PAI.
  submit  Submit your job into PAI.
  token   Update access token.
```

## How to install

```
$ pip install paicli
```

## Practical examples
One can utilize `pai` subcommands to achieve several practical operations.

### Submit multiple jobs with one line

Use `pai submit` and some template engine like [envsubst](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html).

```sh
$ head template.json -n 2
{
  "jobName": "template-${JOBID}"
$ for i in `seq 1 3`; do cat template.json | JOBID=$i envsubst | pai submit; done
```

### Stop multiple jobs with one line

Combine `pai jobs` and `pai stop`.

```sh
$ pai jobs -u sotetsuk -s RUNNING | grep template | awk '{print $1}' | xargs pai stop
```

### Ssh into multiple running containers and run the same command

Combine `pai jobs` and `pai ssh`. In this example, show python processes in multiple jobs with one line.

```sh
$ pai jobs -u sokoya -s RUNNING | grep template | awk '{print $1}' | xargs -n 1 pai ssh -c "ps -aux | grep python"
```

### Show all tensorboard URLs in running jobs

Combine `pai jobs` and `pai host` to show all tensorboard URLs. One can use some browser extention to open all URLs (e.g., [OpenList](https://chrome.google.com/webstore/detail/openlist/nkpjembldfckmdchbdiclhfedcngbgnl?hl=en))

```sh
$ pai jobs -u sotetsuk -s RUNNING | grep template | xargs -n 1 pai host | grep tensorboard | awk '{printf "http://%s:%s\n",$2,$4}'
http://10.0.0.1:9999
http://10.0.0.2:9999
http://10.0.0.3:9999
```

## Config file
To initialize your config file, run `pai config`.
Then your config file will be located in `$HOME/.paicli`.
You should set your `host`, `port`, `api_port` and `username`.
Also, when you update your access token, you should enter your passwrod.

## How to build from source

```sh
$ make build
```

## Author
Sotetsu KOYAMADA
