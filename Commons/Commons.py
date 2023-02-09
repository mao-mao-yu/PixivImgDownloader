import json
import logging
import zipfile
import requests
from Error.Error import *


def json_loader(path) -> str:
    path = path.replace('\\', '/')
    with open(path, 'r', encoding='utf-8') as f:
        txt = json.load(f)
        logging.debug(f"{path} loaded")
    return txt


def loader(path) -> str:
    path = path.replace('\\', '/')
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
        logging.debug(f"{path} loaded")
    return txt


def writer(path, text):
    path = path.replace('\\', '/')
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(text)
    logging.debug(f"The file has been written --> {path} ")


def json_writer(path, text):
    writer(path, json.dumps(text, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))


def binary_writer(path, content):
    path = path.replace('\\', '/')
    with open(path, 'wb+') as f:
        f.write(content)
    logging.debug(f"The file has been written --> {path} ")


def read_zipfile(path) -> zipfile.ZipFile:
    zip_ref = zipfile.ZipFile(path, 'r')
    return zip_ref


def requests_get(url, headers, *args):
    """
    获取网页
    :param url: 要get的网页链接
    :param headers: headers
    :param args:  param
    :return: 类requests.models.Response
    """
    if len(args) > 0:
        params = args[0]
    else:
        params = None
    res = requests.get(url=url, headers=headers, params=params)
    if res.status_code == 200:
        logging.debug(f"Get {url} successful")
        return res
    elif res.status_code == 401:
        raise CookieFailedError(f"Status_code is {res.status_code}, Cookie is failed")
    elif res.status_code == 404:
        raise StatusCodeError(f"Status_code is {res.status_code},Check your id parameter")
    else:
        raise StatusCodeError(f"Status_code is {res.status_code},Check your data")
