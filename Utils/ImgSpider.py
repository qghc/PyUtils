# -*-coding:utf-8-*-
__author__ = '亓根火柴'
import random
import time
import requests
import urllib.parse as urlparse
from bs4 import BeautifulSoup


class FindImgPages:
    # 图片所在的标签标识
    itemBox = ""
    # 标识类型，id，class
    itemBoxType = ""
    # 下一页按钮标识
    nextBtn = ""
    # 标识类型，a
    nextBtnType = ""
    # 访问页
    url = ""
    # 迭代最大次数
    maxCount = 10
    session = None
    encoding = "utf-8"
    nextBtnHead = None

    # 初始化参数
    def init(self,itemBox, itemBoxType, nextBtn, nextBtnType, maxCount):
        self.itemBox = itemBox
        self.itemBoxType = itemBoxType
        self.nextBtn = nextBtn
        self.nextBtnType = nextBtnType
        self.maxCount = maxCount

    def setMore(self, session, encoding, nextBtnHead):
        self.session = session
        self.encoding = encoding
        self.nextBtnHead = nextBtnHead

    # 开始爬取
    def spider(self, url):
        return self.spiderDetail("img", None, None, "src", url)

    # 开始爬取
    def spiderDetail(self, imgTag, imgId, imgIdType, attr, url):
        self.url = url
        if self.session is None:
            self.session = requests.session()
        response = self.session.get(url)
        count = 0
        result = []
        # 记录一下上次的下一页链接，有的网页下一页的连接跟最后一页的连接一样
        lastNext = ""
        while response is not None and count < self.maxCount:
            soup = BeautifulSoup(response.content.decode(self.encoding), "lxml")
            result.extend(self.parseImg(soup, imgTag, imgId, imgIdType, attr))
            response,lastNext = self.loadNextPage(lastNext, self.session, soup)
            count = count+1
            time.sleep(random.randint(1, 1))
        return result

    # 解析图片
    def parseImg(self, soup, imgTag, imgId, imgIdType, attr):
        if self.itemBoxType == "class":
            boxList = soup.find_all(class_=self.itemBox)
        elif self.itemBoxType == "id":
            boxList = soup.find_all(id=self.itemBox)
        result = []
        for box in boxList:
            if imgIdType == "class":
                imgList = box.find_all(imgTag, class_=imgId)
            elif imgIdType == "id":
                imgList = box.find_all(imgTag, id=imgId)
            else:
                imgList = box.find_all(imgTag)
            for img in imgList:
                result.append(img[attr])
                # print(img[attr])
        return result

    # 加载下一页
    def loadNextPage(self, lastNext, session, soup):
        response = None
        btn = None
        if self.nextBtnType == "class":
            btn = soup.find(class_=self.nextBtn)
        elif self.nextBtnType == "id":
            btn = soup.find(id=self.nextBtn)
        elif self.nextBtnType == "text":
            btn = soup.find("a", text=self.nextBtn)
        if btn is not None:
            temp = btn["href"]
            if self.nextBtnHead is not None:
                temp = self.nextBtnHead + temp
            elif temp.startswith('/'):
                result = urlparse.urlparse(self.url)
                temp = result.scheme + "://" + result.netloc + temp
            if lastNext != temp:
                lastNext = temp
                response = session.get(lastNext)
        else:
            print("无下一页")
        return response, lastNext


# fip = FindImgPages()
# fip.init("photo-wp", "class", "next_photo", "id", 2)
# result = fip.spider("https://movie.douban.com/photos/photo/762146744/")
# print(result)

