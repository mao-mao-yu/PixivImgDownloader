import re
import os
import requests
from Error.Error import *
from Commons.Commons import *
from Commons.MyDict import MyDict


class ImageDataGetter:
    def __init__(self, **kwargs):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'referer': 'https://www.pixiv.net'
        }
        self.username = kwargs.pop('username')
        self.password = kwargs.pop('password')
        self.image_size = kwargs.pop('image_size', 'original')
        self.ugoira_size = kwargs.pop('ugoira_size', 'originalSrc')

        self.base_artworks_url = "https://www.pixiv.net/artworks/{}"
        self.base_ugoira_url = "https://www.pixiv.net/ajax/illust/{}/ugoira_meta?lang=zh"
        self.base_user_url = "https://www.pixiv.net/users/{}"
        self.base_user_ajax_url = "https://www.pixiv.net/ajax/user/{}/profile/all?lang=en"
        self.homepage_url = "https://www.pixiv.net"
        self.base_ranking_url = "https://www.pixiv.net/ranking.php"

        self.cookie_path = kwargs.pop("cookie_path", r'./Cookie/cookie.json')
        self.cookie = self._load_cookie()
        self.headers['cookie'] = self.cookie
        self.ugoira_data = None
        self.artist_data = None
        self.artist_id = None

    def get_page_text(self, url: str):
        page_text = self._requests_get(url).text
        return page_text

    def get_response(self, url: str):
        response = self._requests_get(url)
        return response

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
        data = json.loads(self._requests_get(ajax_url).text)
        self.artist_data = MyDict(**data)
        return self.artist_data

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

    def get_image_data(self, image_id: str or int) -> list:
        """
        用re查找到元数据进行解析
        :return: 插画数据
        """
        image_id = str(image_id)
        url = self.base_artworks_url.format(image_id)
        page_text = self.get_page_text(url)
        re_t = """id="meta-preload-data" content='(.*?)'"""
        data_str = re.findall(re_t, page_text)[0]
        data_dic = json.loads(data_str)
        data = MyDict(**data_dic)
        illust_data = data.illust[image_id]
        illust_data = [
            illust_data['illustType'],  # 插画类型
            illust_data.illustTitle,  # 插画title
            illust_data.pageCount,  # 插画张数
            illust_data.urls[self.image_size]  # 对应大小的插画源链接
        ]
        return illust_data

    def get_ugoira_data(self, image_id: str or int) -> MyDict:
        """
        获取动图数据
        """
        image_id = str(image_id)
        url = self.base_ugoira_url.format(image_id)
        data = MyDict(**json.loads(self.get_page_text(url)))
        self.ugoira_data = data
        return data

    def _requests_get(self, url: str, *args) -> requests.Response:
        """
        获取网页
        :param url: 要get的网页链接
        :param args:  param
        :return: 类requests.models.Response
        """
        if len(args) > 0:
            params = args[0]
        else:
            params = None
        res = requests.get(url=url, headers=self.headers, params=params)
        if res.status_code == 200:
            logging.info(f"Get {url} successful")
            return res
        elif res.status_code == 401:
            raise CookieFailedError(f"Status_code is {res.status_code}, Cookie is failed")
        else:
            raise StatusCodeError(f"Status_code is {res.status_code},Check your data")

    def _load_cookie(self) -> str:
        """
        加载cookie
        :return: cookie
        """
        if os.path.exists(self.cookie_path):
            logging.info("Will load cookies")
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
