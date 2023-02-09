import logging
from PixivImageDownloader import PixivScheduler

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    ps = PixivScheduler()
    # ps.rank_mode(mode='daily', content='ugoira', date='20230205')
    data = ps.rank_mode(date=20230206)
    print(data)

