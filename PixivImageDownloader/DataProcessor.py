import os
from Commons.MyDict import MyDict
from Error.Error import SizeNotExistsError
from PixivImageDownloader.ImageDataGetter import ImageDataGetter


class DataProcessor(ImageDataGetter):
    """
    元数据处理器
    """

    def __init__(self, image_size: str, ugoira_size: str, username, password, cookie_path):
        super().__init__(username, password, cookie_path)
        self.image_size = image_size.strip()
        self.ugoira_size = ugoira_size.strip()
        self.ugoira_sizes = ['src', 'originalSrc']
        self.image_sizes = ['mini', 'thumb', 'small', 'regular', 'original']
        self.check_size()

    def check_size(self):
        """
        检查size是否符合参数要求
        """
        if self.ugoira_size not in self.ugoira_sizes:
            raise SizeNotExistsError(f"Ugoira don't have this size -> {self.ugoira_size}")
        if self.image_size not in self.image_sizes:
            raise SizeNotExistsError(f"Image don't have this size -> {self.image_size}")

    @staticmethod
    def get_artist_illustration(artist_data: MyDict) -> list:
        """
        获取画师的所有插画id
        :param artist_data: 画师data数据
        :return: 插画ID list
        """
        illusts = artist_data.body.illusts
        illust_li = [iid for iid, value in illusts.items()]
        return illust_li

    @staticmethod
    def get_artist_manga(artist_data: MyDict) -> list:
        """
        获取画师的所有漫画id
        :param artist_data: 画师data数据
        :return: 漫画ID list
        """
        manga = artist_data.body.manga
        manga_li = [iid for iid, value in manga.items()]
        return manga_li

    @staticmethod
    def get_artist_name(artist_data: MyDict) -> str:
        """
        获取画师名字
        :param artist_data: 画师data
        :return: str name
        """
        artist_name = artist_data.body.pickup[0]['userName']
        return artist_name

    def get_image_url(self, image_data: MyDict) -> str:
        """
        从图片数据获取对应size的url
        """
        urls = image_data.body.urls
        return urls[self.image_size]

    def get_image_urls(self, image_data: MyDict) -> list:
        """
        从图片数据page_count制作单个ID的所有图片url
        """
        url = self.get_image_url(image_data)
        page_count = image_data.body.pageCount
        one_id_urls = [url.replace(f'p0', f'p{i}') for i in range(int(page_count))]
        return one_id_urls

    def get_ugoira_url(self, ugoira_data: MyDict) -> str:
        """
        从动图数据获取动图url
        """
        url = ugoira_data.body[self.ugoira_size]
        return url

    def get_urls(self, datas: list, content: str = None) -> tuple:
        """
        从image_datas获取源链接
        如果content是ugoira则是动图排行榜，会直接从ugoira ajax获取数据
        否则是其他排行榜
        :param datas:图片或者动图数据
        :param content:排行榜content参数
        :return: 图片源链接和帧间隔时间
        """
        if content == 'ugoira':
            images_url = [self.get_ugoira_url(image_data) for image_data in datas]
            durations = [self.get_ugoira_duration(image_data) for image_data in datas]
            urls = images_url
        else:
            images_urls = [self.get_image_urls(image_data) for image_data in datas]
            durations = []
            urls = [url for one_img_urls in images_urls for url in one_img_urls]
        return urls, durations

    def check_url(self, url: str, dir_name: str) -> tuple:
        """
        检查url是不是动图url，如果是动图就获取动图的帧间隔时间和获取动图下载url
        :param url: 图片url
        :param dir_name: 保存路径
        :return: 下载参数
        """
        if 'ugoira' in url:
            img_id = url.split('/')[-1].split('_')[0]
            ugoira_data = self.get_ugoira_data(img_id)
            url = self.get_ugoira_url(ugoira_data)
            duration = self.get_ugoira_duration(ugoira_data)
            filename = img_id + '.gif'
            path = os.path.join(dir_name, filename)
            params = (path, url, duration)
            return params
        else:
            filename = url.split('/')[-1]
            path = os.path.join(dir_name, filename)
            params = (path, url)
            return params

    @staticmethod
    def get_ugoira_duration(ugoira_data: MyDict) -> list:
        duration = [int(d['delay']) / 1000 for d in ugoira_data.body.frames]
        return duration

    @staticmethod
    def get_rank_ids(rank_data: MyDict) -> list:
        contents = rank_data.contents
        illust_ids = [content['illust_id'] for content in contents]
        return illust_ids
