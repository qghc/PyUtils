# -*-coding:utf-8-*-

__author__ = '亓根火柴'
import requests
import time
import logging
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s [%(levelname)s] %(message)s'
)


# 实体类Box，目标信息组所在的box标签
class Box:
    tag = None      # box的标签名
    id = None       # box的id值
    clazz = None    # box的class值
    elements = None # box的目标信息组（Element列表）
    next = None     # box的下一页元素（Element）


# 实体类Element，目标信息元素，它可以表示一个文章中的标题、时间等
class Element:
    tag = None    # 元素的标签名
    index = 0     # 元素的标签索引（一个box中可能会有多个相似的元素）
    id = None     # 元素的id值
    clazz = None  # 元素的class值
    text = None   # 元素的text值（一般用在查找下一页按钮）
    attr = None   # 元素的属性名称（找到该元素后，通过attr获取属性值，如果为None则获取其text）
    prefix = None # 元素的目标值前缀（一般用在获取 相对路径 的文章链接）


class CommonSpider:

    encoding = "utf-8"

    def getItem(self, box, url, session=None, encoding="utf-8"):
        print("访问页：" + url)
        if session is None:
            session = requests.session()
        response = session.get(url)
        time.sleep(26)
        self.encoding = encoding

        # 解析网页，获取数据
        result = self.__getDetail(response.content, box)
        # 获取下一页
        next_url = None
        if box.next is not None:
            next = box.next
            soup = BeautifulSoup(response.content, "lxml", from_encoding=self.encoding)
            next_btn = soup.find(next.tag, id=next.id, class_=next.clazz, text=next.text)
            if next_btn is not None:
                next_url = next.prefix + next_btn["href"]
                time.sleep(1)
        return next_url, result

    def __getDetail(self, content, box):
        soup = BeautifulSoup(content, "lxml", from_encoding=self.encoding)
        # 找到所有的box
        if box.id is not None and box.clazz is not None:
            allBoxes = soup.find_all(box.tag, id=box.id, class_=box.clazz)
        elif box.id is None and box.clazz is not None:
            allBoxes = soup.find_all(box.tag, class_=box.clazz)
        elif box.id is not None and box.clazz is None:
            allBoxes = soup.find_all(box.tag, id=box.id)
        else:
            allBoxes = soup.find_all(box.tag)

        all_result = []
        for item in allBoxes:
            item_result = []
            for element in box.elements:
                # 获取元素标签
                if element.id is not None and element.clazz is not None:
                    tag = item.find_all(element.tag, id=element.id, class_=element.clazz, text=element.text)
                elif element.id is None and element.clazz is not None:
                    tag = item.find_all(element.tag, class_=element.clazz, text=element.text)
                elif element.id is not None and element.clazz is None:
                    tag = item.find_all(element.tag, id=element.id, text=element.text)
                else:
                    tag = item.find_all(element.tag)
                # 按index取值
                if tag is not None and len(tag) > element.index:
                    tag = tag[element.index]
                else:
                    logging.warning("元素[{0}]不存在于[{1}]".format(element.__dict__, item.contents))
                    item_result.append(None)
                    continue
                # 取属性值
                if element.attr is None:
                    info = tag.text.strip()
                else:
                    info = tag[element.attr]
                if element.prefix is not None:
                    info = element.prefix + info
                item_result.append(info)
            all_result.append(item_result)
        return all_result


def test():
    title = Element()
    title.tag = "a"
    title.index = 1

    link = Element()
    link.tag = "a"
    link.index = 1
    link.attr = "href"
    link.prefix = "http://www.bitcoin86.com"

    date = Element()
    date.tag = "time"

    content = Element()
    content.tag = "p"
    content.clazz = "note"

    img = Element()
    img.tag = "img"
    img.clazz = "thumb lazy"
    img.attr = "data-original"

    view = Element()
    view.tag = "span"
    view.clazz = "pv"

    next = Element()
    next.tag = "a"
    next.text = "下一页"
    next.prefix = "http://www.bitcoin86.com/news/"

    box = Box()
    box.tag = "article"
    box.clazz = "excerpt excerpt-1"
    box.elements = [title, link, date, content, img, view]
    box.next = next

    spider = CommonSpider()
    session = requests.session()
    next_url = "http://www.bitcoin86.com/news/"
    while next_url is not None:
        next_url, result = spider.getItem(box, next_url, session)
        print(result)

# test()
