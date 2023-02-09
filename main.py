import logging
from PixivImageDownloader import PixivScheduler, DownloadQueue

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ps = PixivScheduler()
    Q = DownloadQueue()
    Q.add_task(ps.rank_mode(content='illust'))
    Q.add_task(ps.artist_mode(25760573))
    Q.run()
