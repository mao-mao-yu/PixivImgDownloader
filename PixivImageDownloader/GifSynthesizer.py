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
    def synthesize_one(data):
        """
        直接从get的res.content获取文件
        :param data: response.content,duration,path
        :return: 图片二进制数据列表
        """
        path, content, durations = data
        zip_ref = zipfile.ZipFile(io.BytesIO(content))
        list_of_files = zip_ref.namelist()
        img_list = [Image.open(BytesIO(zip_ref.read(filename))) for filename in list_of_files]
        zip_ref.close()
        logging.debug(f"Start synthesize {path}")
        imageio.mimsave(path, img_list, duration=durations)
        logging.debug(f"Synthesize {path} successful")

    @classmethod
    def synthesize_all_with_pool(cls, data_li) -> None:
        pool = Pool(8)
        pool.map(cls.synthesize_one, data_li)
