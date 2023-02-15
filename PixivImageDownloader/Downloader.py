import logging
import threading
from Commons.Commons import requests_get, binary_writer
from PixivImageDownloader.GifSynthesizer import GifSynthesizer
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'referer': 'https://www.pixiv.net'
}


class DownloadQueue:
    """
    下载队列
    """

    def __init__(self, max_workers=8):
        self.threads_queue = []
        self.max_workers = max_workers

    def add_task(self, params_list):
        """
        添加参数到下载队列
        """
        for params in params_list:
            if len(params) == 2:
                self.threads_queue.append(ImgDownloadThread(params))
            elif len(params) == 3:
                self.threads_queue.append(GifDownloadThread(params))

    def run(self):
        """
        开始多线程下载
        """
        logging.info(f"Start downloading all images")
        if self.threads_queue:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                all_tasks = [executor.submit(t.run()) for t in self.threads_queue]
                wait(all_tasks, return_when=ALL_COMPLETED)
        logging.info(f"All images downloaded successfully")


class ImgDownloadThread(threading.Thread):
    """
    多线程图片下载器
    """

    def __init__(self, params):
        threading.Thread.__init__(self)
        self.path, self.url = params
        self.headers = headers

    def run(self):
        res = requests_get(self.url, self.headers)
        binary_writer(self.path, res.content)


class GifDownloadThread(threading.Thread):
    """
    多线程动图下载器
    """

    def __init__(self, params):
        threading.Thread.__init__(self)
        self.path, self.url, self.duration = params
        self.headers = headers

    def run(self):
        content = requests_get(self.url, self.headers).content
        data = (self.path, content, self.duration)
        GifSynthesizer.synthesize_one(data)
