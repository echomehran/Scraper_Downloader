import requests
import subprocess
import getpass
import time
from bs4 import BeautifulSoup as bs
# import argparse # Add Command Line Arguments to a Python Script (switch_flag)


def Login(url, login_route, username, password):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
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


def get_user_input():

    url = input('URL: ')
    username = getpass.getpass('USERNAME: ')
    password = getpass.getpass('PASSWORD: ')
    login_route = input('LOGIN_ROUTE: ')

    return Login(url, login_route, username, password)


def Scraper(page_url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    page = requests.get(
        page_url,
        headers=headers,
    )
    soup = bs(page.text, "html.parser")

    URL_List = []
    link_count = 0
    for a_tag in soup.select('a[href^="/course/"]'):

        links = "https://maktabkhooneh.org" + a_tag["href"]

        URL_List.append(links)
        link_count += 1

    return URL_List


def Donwloader(url_list):

    URL_List = Scraper(url_list)
    download_count = 0

    try:
        for links in URL_List:
            # you can locate the directory you want to store your data with this flage -o ""
            command = f'wget {links}'
            result = subprocess.call(command, shell=True)
            if result == 0:
                download_count += 1

    except KeyboardInterrupt:

        print('Paused ;)')

    return f'\n{download_count} file(s) have been downloaded'


# Sample: https://maktabkhooneh.org/course/%D8%A2%D9%85%D9%88%D8%B2%D8%B4-%D8%B1%D8%A7%DB%8C%DA%AF%D8%A7%D9%86-%DB%8C%D8%A7%D8%AF%DA%AF%DB%8C%D8%B1%DB%8C-%D9%85%D8%A7%D8%B4%DB%8C%D9%86-Andrew-NG-mk1085/%D9%81%D8%B5%D9%84-%D8%A7%D9%88%D9%84-%D9%85%D9%82%D8%AF%D9%85%D9%87-ch3364/%D9%88%DB%8C%D8%AF%DB%8C%D9%88-%D8%AE%D9%88%D8%B4%D8%A2%D9%85%D8%AF%DB%8C%D8%AF-%DB%8C%D8%A7%D8%AF%DA%AF%DB%8C%D8%B1%DB%8C-%D9%85%D8%A7%D8%B4%DB%8C%D9%86/
page_url = input('Please enter the page URL: ')

Login_permission = input('Login required Website [Y], [N]? ')
if Login_permission == 'y' or Login_permission == 'Y':
    get_user_input()

list_len = len(Scraper(page_url))
Download_Permission = input(
    f'\n{list_len} link(s) have been extracted. Do you want to DOWNLOAD them [Y], [N]? ')

Scraper(page_url)

if Download_Permission == 'y' or Download_Permission == 'Y':
    Donwloader(page_url)
else:
    print('\nProcess has been canceled ;)')
