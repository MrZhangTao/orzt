from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User

import os
from app import faker
app = create_app('default')
migrate = Migrate(app, db)

if __name__ == "__main__":
    # app.app_context().push()
    # db.drop_all()
    # 一旦使用"create_all()"将模型映射到数据库中后，即使改变了模型的字段，也不会重新映射了
    # db.create_all()  # 创建表，将模型映射到数据库中
    # faker.users(10)
    # Flask 在 Debug 模式下启动的时候，会被初始化两次
    # 出现这样的问题的原因是在开启 Debug 模式的时候，
    # Werkzeug 默认会 启动一个额外的进程 来监控文件变化以方便重启进程。
    app.run()


