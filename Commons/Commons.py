import json
import logging
import zipfile
import requests
from Error.Error import *


def replace_path(func):
    """
    没什么用 就是把path改成统一格式/
    """

    def wrapper(*args, **kwargs):
        path, *no_need = args
        path = path.replace('\\', '/')
        args = path, *no_need
        return func(*args, **kwargs)
    return wrapper


@replace_path
def json_loader(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        txt = json.load(f)
        logging.debug(f"{path} load successfully")
    return txt


@replace_path
def loader(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
        logging.debug(f"{path} load successfully")
    return txt


@replace_path
def writer(path: str, text: str):
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(text)
    logging.debug(f"{path} download successfully")


@replace_path
def json_writer(path: str, text: str) -> None:
    writer(path, json.dumps(text, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))


@replace_path
def binary_writer(path: str, content: bytes) -> None:
    with open(path, 'wb+') as f:
        f.write(content)
    logging.debug(f"{path} download successfully")


@replace_path
def read_zipfile(path) -> zipfile.ZipFile:
    zip_ref = zipfile.ZipFile(path, 'r')
    return zip_ref


def requests_get(url, headers, params=None):
    """
    获取网页
    :param url: 要get的网页链接
    :param headers: headers
    :param params:  param
    :return: 类requests.models.Response
    """
    res = requests.get(url=url, headers=headers, params=params)
    if res.status_code == 200:
        return res
    elif res.status_code == 401:
        raise CookieFailedError(f"Status_code is {res.status_code}. Cookie is failed ,Check your cookie and reacquire")
    elif res.status_code == 404:
        raise StatusCodeError(f"Status_code is {res.status_code}. Check your id parameter")
    else:
        raise StatusCodeError(f"Status_code is {res.status_code}. Check your data")
