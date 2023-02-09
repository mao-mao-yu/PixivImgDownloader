import multiprocessing
import os
import threading
from Commons.Commons import *
from PixivImageDownloader.GifSynthesizer import *

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'referer': 'https://www.pixiv.net'
}


class DownloadQueue:
    """
    下载队列
    """
    def __init__(self):
        self.threads_queue = []

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
        for t in self.threads_queue:
            t.start()
        for t in self.threads_queue:
            t.join()


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
