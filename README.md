# paicli
A CLI tool for PAI (Platform for AI).

## How to build

```sh
$ make build
```

## How to use

- initialize config file: `$ paicli config`
- submit a job: `$ paicli submit job_config.json`
- ssh to a container: `$ paicli ssh`. Then select a job name (or specify the job name with `-j` option).
- show job list: `$ paicli jobs`
- stop a job: `$ paicli stop`. Then select a job name (or specify the job name with `-j` option)
- generate new access token `$ paicli token` 

## Config file
Your config file will be set in `$HOME/.paicli`.
You should set your `host`, `port`, `api_port` and `username`.
Also, when you update your access token, you should enter your passwrod.

## Author
Sotetsu KOYAMADA
