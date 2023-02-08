import logging
from PixivDownloader.PixivScheduler import PixivScheduler


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    ps = PixivScheduler()
    # data = ps.get_images_urls([105131965, 105135863, 105075398])
    # data = ps.get_ugoira_urls([105135863, 105127803])
    # print(data)
    # ps.rank_mode(mode='daily', content='ugoira', date='20230205')
    ps.rank_mode()

    # ps.artist_mode(25760573)
