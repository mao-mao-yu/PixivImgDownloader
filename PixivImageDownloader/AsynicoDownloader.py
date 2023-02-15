import asyncio
import aiohttp
import logging


class AsyncioDownloadQueue:
    def __init__(self, mask_tasks=20):
        self.params_list = []
        self.headers = None
        self.mask_tasks = mask_tasks

    async def img_download(self, session, path, url):
        pass

    async def gif_download(self, session, path, url, duration):
        pass

    async def run_task(self, session, params):
        pass
