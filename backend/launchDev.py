from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, SpecialData, Text, Picture

import os
from app import faker


if __name__ == "__main__":
    app = create_app('default')
    migrate = Migrate(app, db)

    app.app_context().push()
    db.create_all() # create all tables
    # faker.users(10)
    # faker.specialData()
    faker.texts(10)
    faker.pictures(10)
    # Flask 在 Debug 模式下启动的时候，会被初始化两次
    # 出现这样的问题的原因是在开启 Debug 模式的时候，
    # Werkzeug 默认会 启动一个额外的进程 来监控文件变化以方便重启进程。
    app.run()


