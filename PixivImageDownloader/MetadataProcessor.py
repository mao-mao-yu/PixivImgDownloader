import os
from PixivImageDownloader.ImageDataGetter import ImageDataGetter


class MetadataProcessorData(ImageDataGetter):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.multy_process = kwargs.pop('multy_process', False)
        self.pool_num = kwargs.pop('pool_num', 8)
        self.save_path = os.path.join(
            kwargs.pop('save_path', r"./"),
            'pixiv_img'
        )

    def get_artist_illustration(self, artist_id: str or int) -> list:
        """
        获取画师的所有插画
        :param artist_id: 画师ID
        :return: 插画ID list
        """
        artist_id = str(artist_id)
        if artist_id == self.artist_id:
            artist_data = self.artist_data
        else:
            artist_data = self.get_artist_data(artist_id)
        i_li = artist_data.body.illusts.keys()
        return i_li

    def get_artist_manga(self, artist_id: str or int) -> list:
        """
        获取画师的所有漫画
        :param artist_id: 画师ID
        :return: 漫画ID list
        """
        artist_id = str(artist_id)
        if artist_id == self.artist_id:
            artist_data = self.artist_data
        else:
            artist_data = self.get_artist_data(artist_id)
        m_li = artist_data.body.manga.keys()
        return m_li

    def get_artist_name(self, artist_id: str or int) -> str:
        """
        获取画师名字
        :param artist_id: 画师ID artist id
        :return: str name
        """
        artist_id = str(artist_id)
        if artist_id == self.artist_id:
            artist_data = self.artist_data
        else:
            artist_data = self.get_artist_data(artist_id)
        artist_name = artist_data.body.pickup[0]['userName']
        return artist_name

    def get_images_urls(self, id_li: list) -> list:
        """
        获取多个图片的链接
        :param id_li: 图片ID列表
        :return: 图片url列表
        """
        data_li = [self.get_image_data(image_id) for image_id in id_li]
        urls = []
        for *no_need, p_count, url in data_li:
            one_id_urls = [url.replace(f'p0', f'p{i}') for i in range(int(p_count))]
            urls.append(one_id_urls)
        return urls

    def get_ugoira_duration(self, img_id: str or int) -> list:
        """
        获取动图的帧间隔时间
        :param img_id: 动图ID
        :return: 帧间隔时间的列表
        """
        if self.ugoira_data:
            ugoira_data = self.ugoira_data
        else:
            ugoira_data = self.get_ugoira_data(img_id)
        duration = [int(d['delay']) / 1000 for d in ugoira_data.body.frames]
        return duration

    def get_ugoira_urls(self, id_li: list):
        """
        获取列表内所有动图的zip url和帧间隔时间
        :param id_li: image id list
        :return: [(zip_url1,duration1),(zip_url2,duration2)...]
        """
        urls = []
        for ugoira_id in id_li:
            ugoira_data = self.get_ugoira_data(ugoira_id)
            size = self.ugoira_size
            url = ugoira_data.body[size]
            duration = [int(d['delay']) / 1000 for d in ugoira_data.body.frames]
            urls.append((url, duration))
        return urls
