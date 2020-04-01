#!/usr/bin/env python3

import argparse
import json
from typing import Optional

from dacite import from_dict

from modules.charon import register_webhook_bot
from modules.default_config import UserConfig, ProdConfig, StagingConfig, LocalConfig
from modules.roman import obtain_auth


def fill_missing(cfg: UserConfig, env: Optional[str]):
    if env:
        cfg.env = env

    def set_missing(template):
        cfg.roman_url = cfg.roman_url if cfg.roman_url else template.roman_url
        cfg.charon_url = cfg.charon_url if cfg.charon_url else template.charon_url
        cfg.bot_summary = cfg.bot_summary if cfg.bot_summary else template.bot_summary
        cfg.service_name = cfg.service_name if cfg.service_name else template.service_name

    if cfg.env == 'prod':
        set_missing(ProdConfig())
    elif cfg.env.startswith('stag'):
        set_missing(StagingConfig())
    else:
        set_missing(LocalConfig())


def file_config(path: str) -> UserConfig:
    with open(path, 'r') as file:
        data = json.load(file)
        return from_dict(data_class=UserConfig, data=data)


def args_config(cli_args) -> UserConfig:
    return UserConfig(
        email=cli_args.email,
        password=cli_args.password,
        service_name=cli_args.service_name,
        bot_summary=cli_args.summary,
        env=cli_args.env,
        roman_url=cli_args.roman_url,
        charon_url=cli_args.charon_url
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Register web hook bot in the Wire environment.')
    # for the file configuration
    parser.add_argument("--file", help="Path to configuration JSON.")

    # for the command line configuration
    parser.add_argument("--email", help="Email for the Roman account.")
    parser.add_argument("--password", help="Password for the account.")
    # fall back for loading additional data
    parser.add_argument("--service-name", help="Name of the service, if the account does not exist yet.")
    parser.add_argument("--summary", help="Summary of the service.")
    parser.add_argument("--env", help="From which configuration should be loaded missing values",
                        default='local', choices=['prod', 'staging', 'local'])
    parser.add_argument("--roman-url", help="Roman URL")
    parser.add_argument("--charon-url", help="Charon URL")

    # load config
    args = parser.parse_args()
    config = file_config(args.file) if args.file else args_config(args)
    # fill missing data
    fill_missing(config, args.env)

    auth = obtain_auth(config.roman_url,
                       email=config.email,
                       password=config.password,
                       service_name=config.service_name,
                       service_url=f'{config.charon_url}/roman/messages',
                       service_summary=config.bot_summary)

    if not auth:
        print('It was not possible to get auth token.')
        exit(1)

    r = register_webhook_bot(config.charon_url, bot_api_key=None, auth_code=auth)
    if r:
        print('Bot successfully registered.')
    else:
        print('It was not possible to register bot.')
        exit(2)
