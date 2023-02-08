import os
import re
from Error.Error import *
from Commons.Commons import *
from Commons.MyDict import MyDict
from PixivDownloader.PixivImage import ImageData


class Pixiv(ImageData):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.multy_process = kwargs.pop('multy_process', False)
        self.pool_num = kwargs.pop('pool_num', 8)
        self.save_path = os.path.join(
            kwargs.pop('save_path', r"./"),
            'pixiv_img'
        )
        self.homepage_url = "https://www.pixiv.net"
        self.base_user_url = "https://www.pixiv.net/users/{}"
        self.base_user_ajax_url = "https://www.pixiv.net/ajax/user/{}/profile/all?lang=en"
        self.base_ranking_url = "https://www.pixiv.net/ranking.php"
        self.artist_data = None
        self.artist_id = None

    def get_artist_data(self, artist_id: str or int) -> MyDict:
        """
        获取画师的数据
        :param artist_id: 画师ID
        :return: MyDict
        """
        artist_id = str(artist_id)
        self.artist_id = artist_id
        ajax_url = self.base_user_ajax_url.format(artist_id)
        referer_url = self.base_user_url.format(artist_id)
        self.headers['referer'] = referer_url
        try:
            data = json.loads(self._requests_get(ajax_url).text)
        except CookieFailedError as e:
            print(e)
            self.headers['cookie'] = self._get_cookie()
        else:
            self.artist_data = MyDict(**data)
            return self.artist_data

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

    def get_ranking_data(self, params) -> list:
        """
        获取排行榜里的图片ID
        :param params:
        可设置参数:
        模式 mode: daily , weekly , monthly , male 以及后缀_18 , _ai
        日期 date:默认为昨天 格式20230205
        内容类型 content:illust , ugoira , manga
        页面p 数字
        :return: 返回排行榜图片ID list
        """
        # 获取排行榜页面
        self.headers['referer'] = self.homepage_url
        url = self.base_ranking_url
        page_text = self._requests_get(url, params).text

        # re查找所有插画ID
        i_li = re.findall('href="/artworks/(\d+)"', page_text)
        new_li = []
        # 去重
        [new_li.append(i) for i in i_li if i not in new_li]
        return new_li

    def get_images_urls(self, id_li: list) -> list:
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
