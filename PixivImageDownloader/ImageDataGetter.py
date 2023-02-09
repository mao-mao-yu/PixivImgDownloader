import os
from Commons import *
from Commons.MyDict import MyDict


class ImageDataGetter:
    """
    获取图片相关数据
    """

    def __init__(self, username, password, cookie_path):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'referer': 'https://www.pixiv.net'
        }
        self.base_ugoira_ajax_url = "https://www.pixiv.net/ajax/illust/{}/ugoira_meta"
        self.base_user_ajax_url = "https://www.pixiv.net/ajax/user/{}/profile/all"
        self.base_ranking_url = "https://www.pixiv.net/ranking.php"
        self.base_image_ajax_url = " https://www.pixiv.net/ajax/illust/{}"
        self.username = username
        self.password = password
        self.cookie_path = cookie_path
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
        data = MyDict(**json.loads(requests_get(url, self.headers, params).text))
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
