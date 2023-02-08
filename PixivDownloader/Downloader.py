import os
from Commons.Commons import binary_writer
from multiprocessing.dummy import Pool
from PixivDownloader.PixivMetadataProcessor import PixivMetadataProcessor
from PixivDownloader.GifSynthesizer import GifSynthesizer


class Downloader(PixivMetadataProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def downloader(self, url: str) -> bytes:
        """
        下载单个文件   Download from one url
        :param url: url
        :return: content
        """
        content = self._requests_get(url).content
        return content

    def mp_download(self, u_li: list) -> list:
        """
        多进程下载
        :param u_li: url_list
        :return: 二进制数据列表bytes data list
        """
        self.headers['referer'] = self.homepage_url
        pool = Pool(self.pool_num)
        content_files = pool.map(self.downloader, u_li)
        pool.close()
        pool.join()
        return content_files

    def sp_download(self, u_li: list) -> list:
        """
        单进程下载
        :param u_li: url_list
        :return: 二进制数据列表bytes data list
        """
        self.headers['referer'] = self.homepage_url
        content_files = []
        for url in u_li:
            content_files.append(self.downloader(url))
        return content_files

    def download_with_write(self, params: tuple) -> None:
        """
        下载并保存，如果url为gif的文件会自动合成
        :param params: url path
        :return:
        """
        url, path = params
        path = path.replace("\\", "/")
        dir_path, filename = os.path.split(path)
        img_id = filename.split('_')[0]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if 'ugoira' in url:
            url = url.replace('img-original', 'img-zip-ugoira').replace(filename, f'{img_id}_ugoira1920x1080.zip')
            content = self.downloader(url)
            filename = img_id + '.gif'
            path = os.path.join(dir_path, filename)
            gif = GifSynthesizer()
            duration = self.get_ugoira_duration(img_id)
            data = (path, content, duration)
            gif.synthesize_one(data)
        else:
            content = self.downloader(url)
            binary_writer(path, content)

    def mp_download_with_write(self, data_li: list) -> None:
        """
        多进程下载 multy process downloader
        :param data_li: The url and path list of the data you want to download.
        :return: None
        """
        self.headers['referer'] = self.homepage_url
        pool = Pool(self.pool_num)
        pool.map(self.download_with_write, data_li)
        pool.close()
        pool.join()

    def sp_download_with_write(self, data_li: list) -> None:
        """
        单进程下载 single process downloader
        :param data_li: The url and path list of the data you want to download.
        :return: None
        """
        self.headers['referer'] = self.homepage_url
        for params in data_li:
            self.download_with_write(params)

    def download_all_with_write(self, data_li: list) -> None:
        """
        多进程下载并保存所有
        :param data_li: The url and path list of the data you want to download.
        :return: None
        """
        if self.multy_process:
            self.mp_download_with_write(data_li)
        else:
            self.sp_download_with_write(data_li)

    def download_all(self, u_li: list) -> list:
        """
        下载所有并return二进制数据列表
        :param u_li:
        :return:
        """
        if self.multy_process:
            content_files = self.mp_download(u_li)
        else:
            content_files = self.sp_download(u_li)
        return content_files
