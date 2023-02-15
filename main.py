import logging
from PixivImageDownloader import PixivScheduler, DownloadQueue, ImageDataGetter, DataProcessor

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # I = ImageDataGetter("", "")
    P = PixivScheduler()
    Q = DownloadQueue(max_workers=16)
    # Q.add_task(P.artist_mode(25760573))
    # https://www.pixiv.net/ranking.php?mode=daily&content=illust&date=20230208
    # Q.add_task(P.rank_mode(mode='daily', content='illust', date='20230208'))
    # Q.add_task(P.search_mode("初音ミク"))
    # Q.run()
