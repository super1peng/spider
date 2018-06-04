#coding:utf-8

from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def set_ip_urllib_http():
    proxy = '59.32.94.214:808'
    proxy_handler = ProxyHandler(
        {
            'http':'http://' + proxy,
            'https': 'https://' + proxy,
        }
    )
    opener = build_opener(proxy_handler)

    try:
        response = opener.open('http://httpbin.org/get')
        print(response.read().decode('utf-8'))
    except URLError as e:
        print(e.reason)
    return 0

def set_ip_requests():
    import requests
    proxy = '59.32.94.214:808'
    proxies = {
        'http':'http://' + proxy,
        'https':'https://' + proxy,
    }
    try:
        response = requests.get('http://httpbin.org/get',proxies=proxies)
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)
    return 0

def set_ip_selenium():
    from selenium import webdriver
    proxy = '59.32.94.214:808'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-sever=http://' + proxy)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('http://httpbin.org/get')
    return 0


def main():
    # set_ip_urllib_http()
    # set_ip_requests()
    set_ip_selenium()
    return 0

if __name__ == "__main__":
    main()