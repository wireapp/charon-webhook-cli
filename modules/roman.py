#!/usr/bin/env python3

import os
from typing import Optional

import requests

s = requests.Session()


def silent_print(payload):
    if not os.getenv('SILENT') == 'True':
        print(payload)


def register(url: str, email: str, password: str, service_name: str) -> bool:
    payload = {
        'name': service_name,
        'email': email,
        'password': password
    }
    r = s.post(f"{url}/register", json=payload)
    if r:
        silent_print('Account registered.')
    else:
        silent_print(f'It was not possible to register account: {r.json()}')
    return bool(r)


def login(url: str, email: str, password: str) -> bool:
    payload = {
        'email': email,
        'password': password
    }
    r = s.post(f"{url}/login", json=payload)
    if r:
        silent_print('Login successful.')
    elif r.json().get('message') in {'Authentication failed.'}:
        silent_print(f'It was not possible to login: {r.json()}')
        exit(4)
    else:
        silent_print(f'It was not possible to login: {r.json()}')
    return bool(r)


def create_service(url: str, name: str, service_url: str, service_summary: str) -> Optional[str]:
    payload = {
        'name': name,
        'url': service_url,
        'summary': service_summary if service_summary else 'Summary not provided by user.'
    }
    r = s.post(f"{url}/service", json=payload)
    if r:
        silent_print('Service created.')
        json = r.json()
        silent_print(f'Service has following code:\n{json["service_code"]}')
        return json['service_authentication']
    else:
        silent_print(f'It was not possible to create service: {r.json()}')
        return None


def update_service_url(url: str, service_url: str):
    r = s.put(f'{url}/service', json={'url': service_url})
    if r:
        silent_print(f'URL successfully updated to {service_url}')
    else:
        silent_print('It was not possible to update URL.')


def get_auth_code(url: str, service_url: Optional[str]) -> Optional[str]:
    r = s.get(f'{url}/service')
    if r:
        json = r.json()
        auth_code = json.get('service_authentication')
        if auth_code:
            silent_print('Service exists.')
            silent_print(f'Service has following service code:\n{json["service_code"]}')

            if service_url and json['webhook'] != service_url:
                silent_print(
                    f'Current service URL: {json["webhook"]} does not match provided: {service_url}. Updating.')
                update_service_url(url, service_url)

            return auth_code
        else:
            silent_print('Service does not exist.')
            return None
    else:
        silent_print(f'Error while getting service info: {r.json()}')
        return None


def obtain_auth(url: str, email: str, password: str,
                service_name: Optional[str] = None,
                service_url: Optional[str] = None,
                service_summary: Optional[str] = None) -> Optional[str]:
    """
    Registers bot in the Roman. Returns service_authentication if the registration was successful.
    """

    if login(url, email, password):
        silent_print('Login successful')
    elif register(url, email, password, service_name):
        silent_print('Registration was successful, please check your email and run the script again.')
        return None

    auth_code = get_auth_code(url, service_url)

    if not auth_code:
        auth_code = create_service(url, service_name, service_url, service_summary)

    if not auth_code:
        silent_print('It was not possible to create service.')
        raise Exception('Not possible to obtain auth.')

    return auth_code
