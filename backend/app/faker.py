from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, SpecialData, Text, Picture

'''数据伪造'''
def users(count=10):
    faker = Faker()
    idx = 0
    while idx < count:
        user = User(
            email=faker.email(),
            username=faker.user_name(),
            password="password",
            name=faker.name(),
            sex=randint(0, 1),
            location=faker.city(),
            about_me=faker.text(),
            last_logined = faker.past_date(),
        )
        db.session.add(user)
        try:
            db.session.commit()
            idx += 1
        except IntegrityError as e:
            db.session.rollback()

def specialData():
    user_count = User.query.count()
    for i in range(user_count):
        user = User.query.offset(i).first()
        specialData = SpecialData(
            owner=user,
            owner_id=user.id,
            headuri="wwww.orzt.top",
            bguri="www.orzt.top",
            tags="Interesting",
        )
        db.session.add(specialData)
    db.session.commit()

def texts(count=10):
    print("ssssss")

def pictures(count=10):
    pass
