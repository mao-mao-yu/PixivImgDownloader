import logging
from PixivImageDownloader import PixivScheduler, DownloadQueue, ImageDataGetter, DataProcessor

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # ps = PixivScheduler()
    # Q = DownloadQueue()
    # params_li = ps.rank_mode()
    # params_li1 = ps.artist_mode(25760573)
    # # print(params_li)
    # # print(params_li1)
    # Q.add_task(params_li)
    # Q.add_task(params_li1)
    # Q.run()
    # https://www.pixiv.net/ranking.php?mode=daily&content=illust&date=20230207
    # getter = ImageDataGetter("", "", r"H:\pyproj\learn_python\PixivImgDownloader\Cookie\cookie.json")
    processor = DataProcessor('original', 'originalSrc', "", "",
                              r"H:\pyproj\learn_python\PixivImgDownloader\Cookie\cookie.json")
    params = {
        "order": "popular_d",
        'mode': 'safe',
        's_mode': 's_tag',
        'type': 'ugoira',
        'p': '1',
        'hlt': '1000',
        'wlt': '1000',
    }
    data = processor.search_data(content="初音ミク", params=params)
    # print(data)
    ids = processor.get_searched_data_ids(data)
    # a_data = getter.get_artist_data(25760573)
    # print(len(a_data.body.illusts))
    # params = {
    #     'mode': 'daily',
    #     'date': '20230207',
    #     'content': 'illust',
    #     'p': '1',
    #     'format': 'json'
    # }
    # r_data = getter.get_rank_data(params)
    # print(r_data.contents)
    # for content in r_data.contents:
    #     print(content)
    # i_data = getter.get_image_data(91130567)
    # u_data = getter.get_ugoira_data(105194445)
    # print(i_data)
    # print(u_data)
