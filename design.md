这是一个微信小程序项目——跪了吧(很随意的名字吗？)

        主要的目的是:

                1.不经意间的想法、创意(转瞬即逝)，喜欢的句子段落(可以配图)
                2.存放自己的图片(现在的手机存储的大部分东西吧)
                人并不能将人生中所有有意义开心伤心的事都记忆下来，蓦然回首，尔可解彼时心情乎？

        使用小程序来承载项目的，基于小程序的开发规则，设3个功能页签(最多5个)，置于底部而非顶部
        
                1.idea
                2.おもしろい（日语，有意思)
                3.初心(个人信息页)
                页面布局：日期 + 文本（再加上emoji?),列表格式

----2018年10月27日23:36:41----

先创建项目用数据库，然后思考如何设计表
由于使用flask进行后端的开发，所以想清楚后，使用sqlalchemy表达出来
大致如下:

        用户数据表（当然其实是只有自己一个用户，就是给自己用的):
                用户id， 手机号码，       密码，      昵称，    性别， 居住地
                user_id, telephone,  password,    username, sex, location

        个性数据表:
                数据id， 用户id，   生日，  预估寿命，  头像uri，标签集，背景图片uri，关于自己
                info_id, user_id, birth, lifetime， headuri, tags, bguri， about_me

        记录表:
                    时间，      用户id， 记录id， 标签集，  内容  ， 配图uri， 发表地点
                create_time, user_id, record_id, tags, content， picuri， where

        图片表:
                时间，     用户id，图片id，图片uri，标签集
                create_time, user_id，pic_id,  uri，   tags

----2018年10月28日18:50:30----

数据库相关:

        关于图片或者文件在数据库的存储方式:

                1.把图片直接以二进制形式存储进数据库，比如mysql中有一个blob类型(不建议)
                2.把图片存储在磁盘上，数据库表字段中保存的是图片的路径(推荐)
                => 大字段数据会加重数据库的负担，拖慢数据库(大容量的文本数据也是如此)

                http://www.cnblogs.com/wangtao_20/p/3440570.html
                http://developer.51cto.com/art/201211/364472.htm 的内容之一是：
                三种东西永远不要放到数据库里,图片，文件，二进制数据。作者的理由是，
                        对数据库的读/写的速度永远都赶不上文件系统处理的速度
                        数据库备份变的巨大，越来越耗时间
                        对文件的访问变得麻烦

        在flask中使用mysql数据库，（使用python3）
                首先需要安装pymysql支持，
                然后在配置表config.py里如下设置：
                SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:yourpassword@address:3306/orzt"
        
        ----2018年10月29日11:10:29----

        MYSQL的分页查询是使用关键字: LIMIT offsetN, selectN
        select * from users limit 10, 10;
        缺点：全表扫描，在数据量大的时候，会很慢(Google搜索<数据库分页查询及优化>)
        在flask sqlalchemy里，则是使用query.paginate函数来完成:
                pageV = request.json.get("pageV", 3 , type=int)
                pagination = User.query.paginate(pageV, per_page=current_app.config["XXX_PERPAGE"], error_out=False)
        ----2018年12月06日09:26:14----

        新手使用SQL常犯的五个错误：
        http://www.craigkerstiens.com/2016/06/07/five-mistakes-databases/?utm_source=dbweekly&utm_medium=email

        1.SQL中的User表不应该使用Integer Primary key auto increment,使用uuid是更好好好的选择:
        https://til.hashrocket.com/posts/31a5135e19-generate-a-uuid-in-postgresql
        2.直接把图片或大数据文本存入数据表：应该使用OSS存储资源，然后表中存储url
        3.分页使用 Limit/Offset，应三思
        4.允许使用空值 null，添加新行后，再更新对应的列
                => Default values on new columns
                No matter how long you’ve been at it you won’t get the perfect schema on day 1. It’s better to think of database schemas as continuously evolving documents. Fortunately, it’s easy to add a column to your database, but: it’s also easy to do this in a horrific way. By default, if you just add a column it’ll generally allow NULL values. This operation is fast, but most applications don’t truly want null values in their data, instead they want to set the default value.

                If you do add a column with a default value on the table, this will trigger a full re-write of your table. Note: this is very bad for any sizable table on an application. Instead, it’s far better to allow null values at first so the operation is instant, then set your default, and then, with a background process go and retroactively update the data.

                This is more complicated than it should be
        5.过度拆表(根据应用实际需求，可以接受一定程度的冗余)

        ----2018年11月14日18:05:33----
Flask RESTful设计相关:

        对于flask的HTTP请求上的认证，一般使用Flask-Login扩展来实现用户认证，
        但是如果是Restful API请求的认证，另当别论
                REST系统六条设计规范其中之一提到了：
                => 无状态 => 每个请求必须包含完成请求必需的信息，
                        两次请求之间没有任何相关性，是完全独立的
        所以此时的用户认证使用Flask-HTTPAuth扩展是不错的选择(其他方法:使用flask_jwt)

        ----2018年10月30日09:53:53----

        POSTMAN 使用这个工具来测试接口，更加便捷

        ----2018年10月30日17:43:21----

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

        ----2018年10月30日18:06:31----

        *** RESTful API接口返回数据的格式和风格:
                常见返回的数据的格式一般用JSON。
                对应返回的内容，常见的做法是：
                <<<<<<<<<<<<<>>>>>>>>>>>>>
                code:   http的status code 
                        如果有自己定义的额外的错误，那么也可以考虑用自己定义的错误码
                msg:    对应的文字描述信息
                        如果是出错，则显示具体的错误信息 eg:"invalid access token: wrong or expired"
                        否则操作成功，一般简化处理都是返回OK
                data:
                        对应数据的json字符串
                        如果是数组，则对应最外层是 [] 的list
                        如果是对象，则对应最外层是 {} 的dict

        对于返回值的处理，可以指定需要的字段来作为返回：
                from flask_restful import field, marshal_with, Api, Resource
                在方法上加上带参的装饰器 marshal_with(paramsDict)

        jsonify只能序列化dict和list，不能序列化object，如果直接把模型对象放入:jsonify(obj)，那么需要把obj序列化，模型类内部定义的to_json即是该作用

        ----2018年11月01日15:57:16----

应用登录、验证、认证相关:

        JSON Web Token(缩写JWT) 是一种流行的跨域认证解决方案的产物，这个字符串由服务端生成并返回给客户端保存
        设有变量：A=base64url(header),B=base64url(payload//负载，数据体),C=header.alg(A+"."+B, signature//服务端提供)=>那么jwt=A+"."+B+"."+C ;(base64url算法是可以反推的)
        
        jwt 根本目的是使认证变得安全
        jwt的缺点:
                服务器不保存状态，所以无法在使用过程中废止某个Token，
                一旦签发，在到期前就始终有效，除非服务器设有额外的逻辑处理。
        我认为：jwt在使用完毕后，应手动采用一次性方法将其销毁(比如修改打乱)

        (PS:该博客和jwt无关)
        贴上一则博客: 使用Flask设计RESTful_API的认证
        http://www.pythondoc.com/flask-restful/third.html#id6

        ----2018年10月31日16:17:17----

        查看HttpAuth源码，尤其是login_required内部的传参
                Http Basic认证的安全性并不高，还可以改进
                Http Digest 摘要认证的安全性要高于上者很多

        一个揪心的疑惑解决了：
                使用HttpBasic认证时，在Authorization里传入username和password
                进行第一次认证后，服务器返回一个token，之后的通讯中，
                把token放入username字段作为值，password字段置空，即可通过token验证
                降低每次都使用u 和 p 带来的风险
                疑惑点在于HttpAuth类派生了一个HTTPTokenAuth,然对象仅有1个，于此处理解不通，
                再次阅读上一则博客，解惑矣！

        ----2018年12月06日09:35:39----



