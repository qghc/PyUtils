# -*-coding:utf-8-*-
import logging

__author__ = "亓根火柴"

import requests
import os

logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s [%(levelname)s] %(message)s'
)


class MatchUtils:

    @staticmethod
    def save_img(path=os.getcwd(), name=None, url=None):
        # 校验参数
        if (url is None) or (not url.strip()):
            logging.error("url can't be empty")
            return
        if name is None:
            name = url[url.rindex("/")+1:]
        if not os.path.exists(path):
            os.makedirs(path)
        # 访问网络
        response = requests.get(url)
        if response.status_code != 200:
            logging.error("status_code = [{0}] , url = [{1}]".format(response.status_code, url))
            return
        # 写入文件
        file = open(os.path.join(path, name), "wb+")
        file.write(response.content)
        file.close()

    @staticmethod
    def read_text(path, encoding="utf-8"):
        file = open(path, "r", encoding=encoding)
        lines = file.read()
        file.close()
        return lines

    @staticmethod
    def read_text_lines(path, encoding="utf-8"):
        file = open(path, "r", encoding=encoding)
        lines = file.readlines()
        file.close()
        return lines

    @staticmethod
    def save_text(path, content=str):
        if "/" not in path:
            path = os.path.join(os.getcwd(), path)
        else:
            dir = path[:path.rindex("/")]
            # 创建目录
            if not os.path.exists(dir):
                os.makedirs(dir)
        # 写入文件
        file = open(path, "w+", encoding="utf-8")
        file.write(content)
        file.close()

    @staticmethod
    def append_text(path, content=str):
        if "/" not in path:
            path = os.path.join(os.getcwd(), path)
        else:
            dir = path[:path.rindex("/")]
            # 创建目录
            if not os.path.exists(dir):
                os.makedirs(dir)
        # 写入文件
        file = open(path, "a+", encoding="utf-8")
        file.write(content)
        file.close()

    @staticmethod
    def save_byte(path, content):
        dir = path[:path.rindex("/")]
        # 创建目录
        if not os.path.exists(dir):
            os.makedirs(dir)
        # 写入字节数据
        file = open(path, "wb+")
        file.write(content)
        file.close()

# 测试
# from src.io.MatchUtils import MatchUtils

# MatchUtils.save_img("D:/dd/3/", None, "http://pic.yupoo.com/match7/8152c537/86db77ef.jpg")

# MatchUtils.save_text("D:/dd/4/6/hhs.txt", "传说,女娲娘娘炼就七根火柴,来帮助人类度过第一个冬季,从此,七根火柴散落人间,不见踪迹...")

# MatchUtils.save_byte("D:/dd/4/5/hhs2.txt", b'1wdd')
