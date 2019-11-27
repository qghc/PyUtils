import time
from Test.model.Comment import Comment
from Utils.BaseDao import BaseDao, Page, QueryUtil


def init():
    # 1三种读取配置的方式
    #     1.1默认读取运行文件所在目录下的BaseDao.conf
    #     dao = BaseDao()                        # 当前目录下的BaseDao.conf
    #     dao = BaseDao(conf="./conf/")          # 指定目录下的BaseDao.conf
    #     dao = BaseDao(conf="../conf/db.conf")  # 指定目录下的指定文件
    #
    #     1.2通过构造器读取
    #     dao = BaseDao(user="", password="", database="")
    #
    #     1.3通过字典读取
    #     CONFIG = {
    #         "user": "root",
    #         "password": "root",
    #         "database": "test",
    #         "table": "province"
    #     }
    #     dao = BaseDao(**CONFIG, use_conf=False)

    # 2三种初始化表数据的方式
    #     2.1初始化所有表
    #     dao = BaseDao()
    #
    #     2.2初始化comment表
    #     dao = BaseDao("comment")
    #
    #     2.3初始化多个表，并将第一个表作为默认表
    #     table_list = ["aaa_test", "comment"]
    #     dao = BaseDao(table_list)
    #     dao.change_table(table_list[1])             # 通过此方法变更默认表名
    #     dao.select_all(table_name=table_list[1])    # 或者在执行时指定表名
    #

    # 根据表生成model
    dao = BaseDao("comment")
    dao.generate_model(model_name="Comment")


def insert(user_id, weibo_id, content, remark):
    # 测试插入
    dao = BaseDao("comment")

    comment = Comment()
    comment.user_id = user_id
    comment.weibo_id = weibo_id
    comment.content = content
    comment.remark = remark
    comment.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    dao.save(obj=comment)


def select():
    # 测试查询，指定clazz后，输出为Comment对象列表，可以直接访问其属性
    dao = BaseDao("comment")
    comment_list = dao.select_all(clazz=Comment)
    print(comment_list)

    # 测试按主键查询
    comment = dao.select_pk(primary_key=236, clazz=Comment)
    print(comment.__dict__)

    # 测试按example查询
    example = Comment()
    example.user_id = 124
    example.remark = None
    comment = dao.select_one(filters=example, clazz=Comment)
    print(comment.__dict__)

    # 测试分页
    example = Comment()
    example.user_id = 124
    count = dao.count(filters=example)
    page = Page(page_num=1, page_size=100, total=count)
    while page.hasNext():
        one_page = dao.select_page(page=page, filters=example, clazz=Comment)
        for item in one_page:
            print(item.__dict__)
        page.loadNextPage()


def select_with_condition():
    dao = BaseDao("comment")
    # 测试条件查询，123<=user_id<125
    filters = {
        QueryUtil.GE + "user_id": 123,
        QueryUtil.LT + "user_id": 125,
        QueryUtil.ORDER: "user_id",
        QueryUtil.ORDER_TYPE: "desc"
    }
    comment_list = dao.select_all(filters=filters, clazz=Comment)
    print(comment_list)


def update():
    dao = BaseDao("comment")
    # 按主键修改，会更新空值
    comment = Comment()
    comment.weibo_id = 237
    comment.content = "测试修改4"
    # effect_rows = dao.update_by_primarykey(obj=comment)

    # 按主键修改，不会更新空值
    comment2 = Comment()
    comment2.weibo_id = 236
    comment2.content = "测试修改4"
    effect_rows = dao.update_by_primarikey_selective(obj=comment2)
    print(effect_rows)


def delete():
    dao = BaseDao("comment")
    effect_rows = dao.remove_by_primarykey(value=238)
    print(effect_rows)


if __name__ == '__main__':
    init()
    # insert(123, 234, "Hello world1!", "test insert1")
    # insert(124, 235, "Hello world2!", "test insert2")
    # insert(125, 236, "Hello world3!", "test insert3")
    # insert(124, 237, "Hello world4!", None)
    # select()
    # select_with_condition()
    # update()
    # delete()
