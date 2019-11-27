from Utils.CommonSpider import CommonSpider, Element, Box
from Utils.ImgSpider import FindImgPages
from Utils.MatchUtils import MatchUtils


def testCommonSpider():
    # 测试CommonSpider
    title = Element()
    title.tag = "span"
    title.clazz = "title"
    next = Element()
    next.tag = "a"
    next.text = "后页>"
    next.prefix = "https://movie.douban.com/top250"
    box = Box()
    box.tag = "div"
    box.clazz = "item"
    box.elements = [title]
    box.next = next
    spider = CommonSpider()
    next_url = "https://movie.douban.com/top250"
    while next_url is not None:
        next_url, result = spider.getItem(box, next_url)
        print(result)


# 测试ImgSpider
def testImgSpider():
    fip = FindImgPages()

    fip.init("photo-wp", "class", "next_photo", "id", 2)
    result = fip.spider("https://movie.douban.com/photos/photo/762146744/")
    print(result)


# 测试MatchUtils
def testMatchUtils():
    # MatchUtils.save_img("D:/Test/3/", None, "http://pic.yupoo.com/match7/8152c537/86db77ef.jpg")
    # MatchUtils.save_text("D:/Test/4/6/hhs.txt", "传说,女娲娘娘炼就七根火柴,来帮助人类度过第一个冬季,从此,七根火柴散落人间,不见踪迹...")
    # MatchUtils.save_byte("D:/Test/4/5/hhs2.txt", b'1wdd')
    content = MatchUtils.web_get("http://www.douban.com")
    print(content)


# testCommonSpider()
# testImgSpider()
testMatchUtils()
