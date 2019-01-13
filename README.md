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

- **pai config**: initialize the config file.
- **pai jobs**: show job list.
- **pai token**: generate a new access token.
- **pai submit**: submit a job.
- **pai stop**: stop a job.
- **pai ssh**: ssh into a container.

## Config file
**pai config** will create your config file in `$HOME/.paicli`.
You should set your `host`, `port`, `api_port` and `username`.
Also, when you update your access token, you should enter your passwrod.

## Author
Sotetsu KOYAMADA
