# PyUtils
**一些Python开发中的实用工具。**
    
- Utils
    - BaseDao.conf
    - BaseDao.py
    - CommonSpider.py
    - ImgSpider.py
    - MatchUtils.py

- Test
    - model             
    - BaseDao.conf
    - Test.py
    - TestBaseDao.py

| 文件  |  描述  |
| ----  | ----  |
| BaseDao.conf | BaseDao的配置文件 |
| BaseDao.py | 访问MySQL的工具，可以实现ORM存取。 |
|CommonSpider.py| 通用的网页爬取器，可以简单配置就能爬取网页信息，支持翻页。 |
|ImgSpider.py| 图片爬取器，可以爬取网页中的特定的图片，支持翻页。 |
|MatchUtils.py| 其他一些文件读取，保存图片之类的小工具。 |


| 文件  |  描述  |
| ----  | ----  |
| model | TestBaseDao产生的实体model文件 |
| BaseDao.conf | TestBaseDao的配置文件 |
|TestBaseDao.py| <u>**全面测试BaseDao的功能**</u> |
|Test.py| 测试Util中的其他工具 |

其中，`TestBaseDao.py`是全面测试，也是使用手册，建议先看此文件。