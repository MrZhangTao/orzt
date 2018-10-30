这是一个微信小程序项目——跪了吧(很随意的名字吗？)
主要的目的是:
        1.不经意间的想法、创意(转瞬即逝)，偶尔兴起写一则日记，
        2.存放自己喜欢的句子段落、图片(现在的手机存储的大部分东西吧)，
        3.想说出来但是又没有必要发到类似朋友圈微博的东西(比如发泄用，吐槽)
人并不能将人生中所有有意义开心伤心的事都记忆下来，蓦然回首，尔可解彼时心情乎？

使用小程序来承载项目的，基于小程序的开发规则，设4个功能页签(最多5个)，置于底部而非顶部
        1.idea
        2.おもしろい（日语，有意思)
        3.其实
        4.初心(个人信息页)
        页面布局：日期 + 文本（再加上emoji?),列表格式

----2018年10月27日23:36:41 v0.1----

先创建项目用数据库，然后思考如何设计表
由于使用flask进行后端的开发，所以想清楚后，使用sqlalchemy表达出来
大致如下:
        用户数据表（当然其实是只有自己一个用户，就是给自己用的)：
                id，邮箱，昵称，性别，年龄，生日(死亡倒计时)，
        个性数据表：        
                id，头像，标签集，背景图，
        文本表：
                textId, userid，文本类型，文本标签，时间，文本，
        图片表：
                id，图片uri，图片标签，图片配文

----2018年10月28日18:50:30 v0.2----

关于图片或者文件在数据库的存储方式：
        1.把图片直接以二进制形式存储进数据库，比如mysql中有一个blob类型(不建议)
        2.把图片存储在磁盘上，数据库表字段中保存的是图片的路径(推荐)
        => 大字段数据会加重数据库的负担，拖慢数据库(大容量的文本数据也是如此)

        http://www.cnblogs.com/wangtao_20/p/3440570.html
        http://developer.51cto.com/art/201211/364472.htm 的内容之一是：
        三种东西永远不要放到数据库里,图片，文件，二进制数据。作者的理由是，
                对数据库的读/写的速度永远都赶不上文件系统处理的速度
                数据库备份变的巨大，越来越耗时间
                对文件的访问需要穿越你的应用层和数据库层

在flask中使用mysql数据库，（使用python3）
        首先需要安装pymysql支持，
        然后在配置表config.py里如下设置：
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:yourpassword@address:3306/orzt"
        
----2018年10月29日11:10:29 v0.3----

对于flask的HTTP请求上的认证，一般使用Flask-Login扩展来实现用户认证，
但是如果是Restful API请求的认证，另当别论
        REST系统六条设计规范其中之一提到了：
        => 无状态 => 每个请求必须包含完成请求必需的信息，
                两次请求之间没有任何相关性，是完全独立的
所以此时的用户认证使用Flask-HTTPAuth扩展是不错的选择(可能还存在其他方法)

----2018年10月30日09:53:53 v0.4----

POSTMAN 使用这个工具来测试接口，更加便捷

----2018年10月30日17:43:21 v0.5----

Flask-RESTful扩展提供了一个RequestParser类来处理数据验证
from flask_restful import reqparse
reqparser = reqparse.RequestParser() # create a instance

POST 和 PUT 方法 是需要接收参数的:
reqparser.add_argument("argName",
                        type=typeName,
                        location=locationName, # 默认是values,在本项目中应为json
                        required=True, # 如果必须要，就加上该关键字参数
                        default=defVal,
                        help="if this arg does not exist, " # 缺少提示
                        "you will get this msg")

----2018年10月30日18:06:31 v0.6----