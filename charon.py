#!/usr/bin/env python3
from typing import Optional

import requests


def register_webhook_bot(charon_url: str, bot_api_key: Optional[str], auth_code: str) -> bool:
    """"
    Registers web hook bot in the charon. Returns True if the registration was success.
    """
    payload = {
        "bot_api_key": bot_api_key if bot_api_key else '',
        "authentication_code": auth_code
    }
    r = requests.post(f'{charon_url}/registration/hook', json=payload)
    if r:
        print('Bot registered')
    else:
        print(f'It was not possible to register the bot: {r.json()}')

    return bool(r)
