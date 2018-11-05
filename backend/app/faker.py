from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, ExtraInfo, Record, Picture

'''数据伪造'''
def users(count=10):
    faker = Faker("zh_CN")
    idx = 0
    while idx < count:
        # user
        user = User(
            telephone=str(faker.phone_number()),
            password="password",
            username=faker.user_name(),
            name=faker.name(),
            sex=randint(0, 1),
            location=faker.city_name(),
        )
        db.session.add(user)
        try:
            db.session.commit()
            print(user)
            idx += 1
        except IntegrityError as e:
            print("error :=> db.session.rollback()")
            db.session.rollback()
    # __extrainfo()

def __extrainfo():
    faker = Faker("zh_CN")
    for user in User.query.all():
        print(user)
        # extrainfo
        extrainfo = ExtraInfo(
            user_id=user.user_id,
            birth=faker.date_this_century(),
            about_me=faker.sentence(),
        )
        user.extrainfo = extrainfo
        db.session.add(user)
        db.session.commit()
        # some records
        for i in range(randint(1, 3)):
            record = Record(
                user_id=user.user_id,
                where=faker.address(),
                content=faker.sentence(),
            )
            db.session.add(record)
        db.session.commit()
        # some pictures
    
