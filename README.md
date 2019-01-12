# paicli
A CLI tool for PAI (Platform for AI).

## How to install

```
$ pip install paicli
```

## How to build

```sh
$ make build
```

## Commands

- **pai config**: initialize config file.
- **pai jobs**: show job list.
- **pai token**: generate new access token.
- **pai submit**: submit a job.
- **pai stop**: stop a job.
- **pai ssh**: ssh to a container.

## Config file
Your config file will be set in `$HOME/.paicli`.
You should set your `host`, `port`, `api_port` and `username`.
Also, when you update your access token, you should enter your passwrod.

## Author
Sotetsu KOYAMADA
