from Utils.BaseDao import BaseDao, Page

from Utils.CommonSpider import CommonSpider, Element, Box
from Utils.ImgSpider import findImgPages
from Utils.MatchUtils import MatchUtils


class Comment:
    user_id = None
    weibo_id = None
    content = None
    remark = None
    time = None


# 测试BaseDao
def test_BaseDao():
    dao = BaseDao("comment")
    result = dao.select_one(clazz=Comment)
    print(result.user_id)
    print(result.__dict__)
    # 测试分页
    count = dao.count()
    page = Page(page_num=1, page_size=100, total=count)
    while page.page_num <= page.pages:
        one_page = dao.select_page(page=page, clazz=Comment)
        for item in one_page:
            print(item.__dict__)
        page.loadNextPage()


def test_CommonSpider():
    global result
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
def test_ImgSpider():
    fip = findImgPages()

    fip.init("photo-wp", "class", "next_photo", "id", 16)
    result = fip.spider("https://movie.douban.com/photos/photo/762146744/")
    print(result)


# 测试MatchUtils
def test_MatchUtils():
    MatchUtils.save_img("D:/dd/3/", None, "http://pic.yupoo.com/match7/8152c537/86db77ef.jpg")
    MatchUtils.save_text("D:/dd/4/6/hhs.txt", "传说,女娲娘娘炼就七根火柴,来帮助人类度过第一个冬季,从此,七根火柴散落人间,不见踪迹...")
    MatchUtils.save_byte("D:/dd/4/5/hhs2.txt", b'1wdd')


test_BaseDao()
# test_CommonSpider()
# test_ImgSpider()
# test_MatchUtils()


