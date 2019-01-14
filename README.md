[![PyPI version](https://badge.fury.io/py/paicli.svg)](https://badge.fury.io/py/paicli)
[![License MIT](https://img.shields.io/github/license/sotetsuk/paicli.svg)](https://github.com/sotetsuk/paicli/blob/master/LICENSE)

# paicli
A CLI tool for [OpenPAI](https://github.com/microsoft/pai).

## How to install

```
$ pip install paicli
```

## Commands

- **pai config**: initialize the config file.
- **pai jobs**: show job list.
- **pai token**: generate a new access token.
- **pai submit**: submit a job.
- **pai stop**: stop a job.
- **pai ssh**: ssh into a container.
- **pai host**: show ip/port information of a job.

## Config file
**pai config** will create your config file in `$HOME/.paicli`.
You should set your `host`, `port`, `api_port` and `username`.
Also, when you update your access token, you should enter your passwrod.

## How to build from source

```sh
$ make build
```

## Author
Sotetsu KOYAMADA
