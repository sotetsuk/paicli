# paicli
A CLI tool for PAI (Platform for AI).

## How to build

```sh
$ make build
```

## How to use

- submit a job: `$ paicli submit job_config.json`
- ssh to a container: `$ paicli ssh`. Then select a job name (or specify the job name with `-j` option).
- show job list: `$ paicli jobs`
- stop a job: `$ paicli stop`. Then select a job name ()or specify the job name with `-j` option)
- generate new access token `$ paicli token` 


## Author
Sotetsu KOYAMADA