import os
import time
import logging
from Error.Error import FuncNotExistsError
from PixivDownloader.Downloader import Downloader
from PixivDownloader.GifSynthesizer import GifSynthesizer


class PixivScheduler(Downloader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.durations = None

    def rank_urls_and_paths(self, **kwargs) -> list:
        """
        获取排行榜图片源链接和保存路径
        :param kwargs: Look Pixiv.get_ranking_data
        :return: pic data [(pic1,pic1_path),(pic2,pic2_path),(pic2,pic2_path2)]
        """
        params = dict(kwargs)
        mode = params.get('mode', 'daily')
        date = params.get('date', str(int(time.strftime("%Y%m%d")) - 1))
        content = params.get('content', "overall")
        dir_name = f"rank/{mode}_{date}_{content}"
        id_li = self.get_ranking_data(params=params)
        if params.get('content') == "ugoira":
            logging.info("Start get zip url")
            data_li = self.get_ugoira_urls(id_li)
            path = os.path.join(self.save_path, dir_name)
            urls_paths = [(url, os.path.join(path, url.split('/')[-1].split('_')[0]) + '.gif') for url, ds in
                          data_li]
            self.durations = [ds for url, ds in data_li]
            logging.info("Get zip url success")
            return urls_paths
        else:
            logging.info("Start get image url")
            u_li = self.get_images_urls(id_li)
            path = os.path.join(self.save_path, dir_name)
            urls_paths = [(url, os.path.join(path, url.split('/')[-1])) for urls in u_li for url in urls]
            logging.info("Get image url success")
            return urls_paths

    def artist_urls_and_paths(self, artist_id: str or int, content: str) -> list:
        """
        通过画师ID获取插画id并处理为图片url和保存路径 Get all works of the artist
        :artist_id 画师ID :artist_id: artist id
        :content 有illust和manga两个参数，content: content illustration or manga
        :return: pic data [(pic1_url,pic1_path),(pic2_url,pic2_path),(pic2_url,pic2_path2)]
        """
        if content.strip() == 'illust':
            func = self.get_artist_illustration
        elif content.strip() == 'manga':
            func = self.get_artist_manga
        else:
            raise FuncNotExistsError(f"Don't have this func:{content}")
        id_li = func(artist_id)
        u_li = self.get_images_urls(id_li)
        artist_name = self.get_artist_name(artist_id)
        dir_path = os.path.join(self.save_path, 'artist')
        symbols = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        cleaned_artist_name = "".join([char for char in artist_name if char not in symbols])
        path = os.path.join(dir_path, cleaned_artist_name)
        urls_and_paths = [(url, os.path.join(path, url.split('/')[-1])) for urls in u_li for url in urls]
        return urls_and_paths

    def rank_mode(self, **kwargs) -> None:
        """
        下载排行榜图片，Download rank images
        :param kwargs:
        可设置参数:
        模式 mode: daily , weekly , monthly , male 以及后缀_18 , _ai
        日期 date:默认为昨天 格式 20230205
        排行榜类型 url content: illust , ugoira , manga
        页面p 数字  page num
        :return:
        """
        urls_paths = self.rank_urls_and_paths(**kwargs)
        if self.durations:
            # 如果有durations帧间隔时间参数则是动图排行榜
            gs = GifSynthesizer()
            durations = self.durations
            self.durations = None
            u_li, p_li = [], []
            [(u_li.append(zip_url), p_li.append(path)) for zip_url, path in urls_paths]
            # 开始下载所有zip
            logging.info("Start downloading rank")
            content_li = self.download_all(u_li)
            logging.info("Download successful")
            # 多进程合成gif
            logging.info("Start synthesizing gif")
            if self.multy_process:
                gs.synthesize_all_with_pool(content_li, p_li, durations)
            else:
                gs.synthesize_all(content_li, p_li, durations)
            logging.info("Synthetic gif successful")
        else:
            # 否则是普通插图排行榜
            logging.info("Start downloading rank")
            self.download_all_with_write(urls_paths)
            logging.info("Download successful")

    def artist_mode(self, artist_id: int or str, content: str = 'illust') -> None:
        """
        下载画师所有作品
        :param artist_id:
        :param content:
        :return:
        """
        urls_paths = self.artist_urls_and_paths(artist_id, content)
        logging.info("Start downloading all works of the artist")
        self.download_all_with_write(urls_paths)
        logging.info("Download all images successful")
