from PixivImageDownloader import *
from Commons import *
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'referer': 'https://www.pixiv.net'
}
DP = DataProcessor('original', 'originalSrc', "", "", r"H:\pyproj\learn_python\PixivImgDownloader\Cookie\cookie.json")
data = DP.get_artist_data(25760573)
ids = DP.get_artist_illustration(data)
base_url = "https://www.pixiv.net/ajax/illust/{}"


async def requests_get(url, headers, params=None, semaphore: Semaphore=None):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                return await response.text()

async def run_tasks(tasks, max_workers):
    semaphore = Semaphore(max_workers)
    return await asyncio.gather(*[requests_get(*task, semaphore=semaphore) for task in tasks])

async def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'referer': 'https://www.pixiv.net'
    }
    base_url = "https://www.pixiv.net/ajax/illust/{}"
    tasks = [(base_url.format(img_id), headers) for img_id in ids]
    texts = await run_tasks(tasks=tasks, max_workers=2)
    return texts


texts = asyncio.run(main())


json_datas = [json.loads(text) for text in texts]
urls = [data['body']['urls']['original'] for data in json_datas]
print(urls)
