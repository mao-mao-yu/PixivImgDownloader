import json
import logging
import zipfile


def json_loader(path) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        txt = json.load(f)
        logging.info(f"{path} loaded")
    return txt


def loader(path) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
        logging.info(f"{path} loaded")
    return txt


def writer(path, text):
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(text)
    logging.info(f"The file has been written --> {path} ")


def json_writer(path, text):
    writer(path, json.dumps(text, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))


def binary_writer(path, content):
    with open(path, 'wb+') as f:
        f.write(content)
    logging.info(f"The file has been written --> {path} ")


def read_zipfile(path) -> zipfile.ZipFile:
    zip_ref = zipfile.ZipFile(path, 'r')
    return zip_ref
