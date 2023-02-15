import os
import json
import logging
from Error.Error import ParamsError
from Commons import requests_get, json_loader, json_writer
from Commons.MyDict import MyDict


class ImageDataGetter:
    """
    获取图片相关数据
    """

    def __init__(self, username, password):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'referer': 'https://www.pixiv.net'
        }
        self.base_ugoira_ajax_url = "https://www.pixiv.net/ajax/illust/{}/ugoira_meta"
        self.base_user_ajax_url = "https://www.pixiv.net/ajax/user/{}/profile/all"
        self.base_ranking_url = "https://www.pixiv.net/ranking.php"
        self.base_image_ajax_url = "https://www.pixiv.net/ajax/illust/{}"

        self.base_s_artworks_ajax_url = "https://www.pixiv.net/ajax/search/artworks/{}"
        self.base_s_illustrations_ajax_url = "https://www.pixiv.net/ajax/search/illustrations/{}"
        self.base_s_manga_ajax_url = "https://www.pixiv.net/ajax/search/manga/{}"

        self.username = username
        self.password = password
        self.cookie_path = os.path.join(os.path.dirname(__file__), '..', 'Cookie/cookie.json')
        self.cookie = self._load_cookie()
        self.headers['cookie'] = self.cookie

    def get_artist_data(self, artist_id: str or int) -> MyDict:
        """
        ajax获取画师的数据
        :param artist_id: 画师ID
        :return: MyDict
        """
        artist_id = str(artist_id)
        url = self.base_user_ajax_url.format(artist_id)
        data = MyDict(**json.loads(requests_get(url, self.headers).text))
        return data

    def get_rank_data(self, params: dict) -> MyDict:
        """
        "https://www.pixiv.net/ranking.php"获取排行榜数据
        :param params:
        可设置参数:
        模式 mode: daily , weekly , monthly , male 以及后缀_18 , _ai
        日期 date:默认为昨天 格式20230205
        内容类型 content:illust , ugoira , manga
        页面p 数字
        格式format: json
        :return: 返回排行榜图片ID list
        """
        # 获取排行榜页面
        url = self.base_ranking_url
        page_text = requests_get(url, self.headers, params).text
        data = MyDict(**json.loads(page_text))
        return data

    def search_data(self, content: str, params: dict) -> MyDict:
        """
        搜索获取作品
        s_artworks_ajax_url = "https://www.pixiv.net/ajax/search/artworks/{}?word={}"
        s_illustrations_ajax_url = "https://www.pixiv.net/ajax/search/illustrations/{}?word={}"
        s_manga_ajax_url = "https://www.pixiv.net/ajax/search/manga/{}?word={}"
        :param content:关键词
        :param params:
        params = {
        "order": "popular_d",
        'mode': 'safe',
        's_mode': 's_tag_full',
        'type': 'all',
        'p': '1',
        'hlt': '1000',
        'wlt': '1000',
        'scd': '2022-02-03'
        }
        order: date_d按新排序,date按旧排序,会员:全站受欢迎popular_d,受男性欢迎popular_male_d,受女性欢迎popular_female_d
        p: page num 第几页
        mode: safe or r18
        s_mode: 关键词与标签部分一致s_tag，完全一致s_tag_full，标题说明文字s_tc
        type:
        artworks_url all所有，
        illustrations_url illust插画，插画动态插画 illust_and_ugoira,动图ugoira
        manga_url manga漫画
        blt bgt: blt=100 100收藏以上 bgt=100 收藏100以下
        wlt,wgt: weight上下限 wlt=1000 weight1000以上 wgt=2999 weight2999以下
        hlt,hgt: Height 上下限 hlt=1000 Height1000以上 hgt=2999 Height2999以下
        scd : 2023-02-03 从20230203到今天的日期以内投稿的
        :return: Mydict的搜索数据
        """
        type_str = params.get('type').strip()
        if 'all' in type_str:
            base_url = self.base_s_artworks_ajax_url
        elif 'illust' in type_str or 'ugoira' in type_str:
            base_url = self.base_s_illustrations_ajax_url
        elif 'manga' in type_str:
            base_url = self.base_s_manga_ajax_url
        else:
            raise ParamsError(f"Search params type:{type_str} not exists")
        url = base_url.format(content, content)
        data = MyDict(**json.loads(requests_get(url, self.headers, params=params).text))
        return data

    def get_image_data(self, image_id: str or int) -> MyDict:
        """
        ajax获取插画数据
        :param image_id:图片ID
        :return: 插画数据
        """
        image_id = str(image_id)
        url = self.base_image_ajax_url.format(image_id)
        data = MyDict(**json.loads(requests_get(url, self.headers).text))
        return data

    def get_ugoira_data(self, image_id: str or int) -> MyDict:
        """
        ajax获取动图数据
        :param image_id: 动图ID
        :return: Mydict的动图数据
        """
        image_id = str(image_id)
        url = self.base_ugoira_ajax_url.format(image_id)
        data = MyDict(**json.loads(requests_get(url, self.headers).text))
        return data

    def _load_cookie(self) -> str:
        """
        加载本地cookie
        :return: cookie
        """
        self.username = self.username.strip()
        self.password = self.password.strip()
        if os.path.exists(self.cookie_path):
            return json_loader(self.cookie_path)
        else:
            logging.info("Cookies file not exists,Will get Cookies")
            if self.username and self.password:
                cookie = self._get_cookie()
            else:
                self.username = input("Please enter your pixiv username")
                self.password = input("please enter your pixiv password")
                cookie = self._get_cookie()
            return cookie

    def _get_cookie(self) -> str:
        """
        获取cookie
        :return: cookie
        """
        from Commons import GetCookie
        path = os.path.split(self.cookie_path)[0]
        if not os.path.exists(path):
            os.makedirs(path)
        cookie = GetCookie.get_cookie(self.username, self.password)
        json_writer(self.cookie_path, cookie)
        return cookie
