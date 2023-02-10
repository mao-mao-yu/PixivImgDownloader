import os
import time
from PixivImageDownloader.Downloader import *
from PixivImageDownloader.DataProcessor import DataProcessor


class PixivScheduler:
    """
    调度器
    """

    def __init__(self, **kwargs):
        self.username = kwargs.pop('username', "")
        self.password = kwargs.pop('password', "")
        self.save_path = kwargs.pop('save_path', "./pixiv_img")
        self.cookie_path = kwargs.pop('cookie_path', r'./Cookie/cookie.json')
        self.image_size = kwargs.pop('image_size', 'original')
        self.ugoira_size = kwargs.pop('ugoira_size', 'originalSrc')
        self.data_processor = DataProcessor(self.image_size,
                                            self.ugoira_size,
                                            self.username,
                                            self.password,
                                            self.cookie_path)

    def rank_mode(self, **kwargs) -> list:
        """
        排行榜下载模式
        :return:返回下载需要的参数
        """
        mode = kwargs.pop('mode', 'daily')
        date = kwargs.pop('date', str(int(time.strftime("%Y%m%d")) - 1))
        content = kwargs.pop('content', None)
        p = kwargs.pop('p', '1')
        url_params = {'mode': mode, 'date': date, 'content': content, 'p': p, 'format': 'json'}
        rank_data = self.data_processor.get_rank_data(url_params)
        if content is None:
            dir_name = os.path.join(self.save_path, 'rank_mode', f"{mode}_{date}_{p}")
        else:
            dir_name = os.path.join(self.save_path, 'rank_mode', f"{mode}_{date}_{content}_{p}")
        ids = self.data_processor.get_rank_ids(rank_data)

        logging.info(f"Start get image data")
        if content == 'ugoira':  # 这里写成这样主要是因为如果排行榜模式是ugoira就不用去再一个一个检查ID是不是动图了直接获取ugoira数据
            image_datas = [self.data_processor.get_ugoira_data(img_id) for img_id in ids]
        else:
            image_datas = [self.data_processor.get_image_data(img_id) for img_id in ids]
        urls, durations = self.data_processor.get_urls(image_datas, content)
        if not durations:  # 如果durations有元素则是ugoira排行榜
            params_list = [self.data_processor.check_url(url, dir_name) for url in urls]
        else:
            paths = [os.path.join(dir_name, url.split('/')[-1]) for url in urls]
            params_list = [(paths[i], url, durations[i]) for i, url in enumerate(urls)]
        logging.info(f"All data get successfully")

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        return params_list

    def artist_mode(self, artist_id: str or int, content: str = "illust") -> list:
        """
        画师下载模式
        :return:返回下载需要的参数
        """
        artist_data = self.data_processor.get_artist_data(artist_id)
        artist_name = self.data_processor.get_artist_name(artist_data)
        dir_name = os.path.join(self.save_path, 'artist_mode', artist_name)
        if content == 'illust':
            ids = self.data_processor.get_artist_illustration(artist_data)
        elif content == 'manga':
            ids = self.data_processor.get_artist_manga(artist_data)
        else:
            raise ContentNotExistsError(f"Artist don't have {content} works")
        if len(ids) == 0:
            raise ContentNotExistsError(f"Artist don't have {content} works")

        logging.info(f"Start get image data")
        images_data = [self.data_processor.get_image_data(img_id) for img_id in ids]
        urls, *no_need = self.data_processor.get_urls(images_data)
        params_list = [self.data_processor.check_url(url, dir_name) for url in urls]
        logging.info(f"All data get successfully")

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        return params_list

    def search_mode(self, keywords, **kwargs):
        """
        params = {
        "order": "popular_d",
        'mode': 'safe',
        's_mode': 's_tag',
        'type': 'ugoira',
        'p': '1',
        'hlt': '1000',
        'wlt': '1000',
        }
        """
        order = kwargs.pop('order', 'popular_d').strip()
        mode = kwargs.pop('mode', 'safe').strip()
        s_mode = kwargs.pop('s_mode', 's_tag').strip()
        type_str = kwargs.pop('type', 'illust').strip()
        p = kwargs.pop('p', '1').strip()
        hlt = kwargs.pop('hlt', '1000').strip()
        wlt = kwargs.pop('hlt', '1000').strip()
        params = {
            "order": order,
            'mode': mode,
            's_mode': s_mode,
            'type': type_str,
            'p': p,
            'hlt': hlt,
            'wlt': wlt,
        }
        data = self.data_processor.search_data(keywords, params)
        dir_name = os.path.join(self.save_path, 'search_mode', keywords)
        ids = self.data_processor.get_searched_data_ids(data)

        logging.info(f"Start get image data")
        images_data = [self.data_processor.get_image_data(img_id) for img_id in ids]
        urls, *no_need = self.data_processor.get_urls(images_data)
        params_list = [self.data_processor.check_url(url, dir_name) for url in urls]
        logging.info(f"All data get successfully")

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        return params_list
