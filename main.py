import logging
from PixivDownloader import PixivScheduler


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    ps = PixivScheduler()
    # ps.rank_mode(mode='daily', content='ugoira', date='20230205')
    ps.rank_mode()

    # ps.artist_mode(25760573)
