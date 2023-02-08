import io
import logging
import zipfile
import imageio
from PIL import Image
from io import BytesIO
from multiprocessing.dummy import Pool
from Commons.Commons import read_zipfile


class GifSynthesizer:
    """
    GIF合成器 Gif Synthesizer
    """
    @staticmethod
    def load_all_images(path: str) -> list:
        """
        从本地获取压缩文件
        :param path: 压缩文件path, zip path
        :return: 图片二进制数据列表,img_list
        """
        zip_ref = read_zipfile(path)
        list_of_files = zip_ref.namelist()
        img_list = []
        for filename in list_of_files:
            img = Image.open(BytesIO(zip_ref.read(filename)))
            img_list.append(img)
        zip_ref.close()
        return img_list

    @staticmethod
    def get_all_images(content: bytes) -> list:
        """
        直接从get的res.content获取文件
        :param content: requests.get.response
        :return: 图片二进制数据列表
        """
        zip_ref = zipfile.ZipFile(io.BytesIO(content))
        list_of_files = zip_ref.namelist()
        img_list = []
        for filename in list_of_files:
            img = Image.open(BytesIO(zip_ref.read(filename)))
            img_list.append(img)
        zip_ref.close()
        return img_list

    def synthesize_all(self, content_li: list, paths: list, durations: list) -> None:
        """
        单线程合成所有gif
        :param content_li: 压缩文件二进制数据
        :param paths: 保存路径
        :param durations: 帧间时间间隔
        :return: None
        """
        for i, content in enumerate(content_li):
            logging.info(f"Now synthesizing the {i}")
            img_list = self.get_all_images(content)
            data = (paths[i], img_list, durations[i])
            self.synthesize_one(data)

    def synthesize_one(self, data: tuple) -> None:
        """
        合成单个gif
        :param data: 保存路径，图片二进制数据，帧间隔时间， path,img binary data, delay
        :return: None
        """
        path, content, duration = data
        logging.info(f"Now synthesizing the {path.split('/')[-1]}")
        img_list = self.get_all_images(content)
        save_path = path.replace("\\", "/")
        imageio.mimsave(save_path, img_list, duration=duration)

    def synthesize_all_with_pool(self, content_li: list, paths: list, durations: list) -> None:
        data_li = []
        for i, content in enumerate(content_li):
            data_li.append((paths[i], content, durations[i]))
        pool = Pool(8)
        pool.map(self.synthesize_one, data_li)

