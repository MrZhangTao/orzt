from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, SpecialData, Text, Picture

import os
from app import faker

app = create_app('default')
migrate = Migrate(app, db)

app.app_context().push()
db.create_all() # create all tables
# faker.users(10)
# faker.specialData()
faker.texts(10)
faker.pictures(10)
app.run()

