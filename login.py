import requests
import getpass
import time
# import argparse # Add Command Line Arguments to a Python Script (switch_flag)


def Login(url, login_route, username, password):

    headers = {
        'User-Agent': '', # ! DO NOT Forget complete the user-agent part
        'origin': url,
        'referer': url + login_route,
    }

    request_session = requests.session()

    csrf_token = request_session.get(url).cookies['csrftoken']

    login_payload = {
        'hidden_username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }

    login_request = request_session.post(
        url + login_route, headers=headers, data=login_payload)

    # *** CSRF_token is in cookies, we can print cookies variable to see csrf_token and other stuff

    if login_request.status_code == 200:
        msg = f'\nYou have logged in successfully {login_request.status_code}'
    else:
        msg = f'\nError {login_request.status_code}'

    print(msg)
