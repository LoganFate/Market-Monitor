from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash


# Adds a demo user, you can add other users here if you want
def seed_users():
    users = [
        User(
            username='DemoUser1',
            email='demo1@example.com',
            password=generate_password_hash('password1'),
            name='Demo User 1',
            user_about='About Demo User 1',
            profile_pic='/path/to/profile1.jpg'
        ),
        User(
            username='DemoUser2',
            email='demo2@example.com',
            password=generate_password_hash('password2'),
            name='Demo User 2',
            user_about='About Demo User 2',
            profile_pic='/path/to/profile2.jpg'
        ),
        User(
            username='DemoUser3',
            email='demo3@example.com',
            password=generate_password_hash('password3'),
            name='Demo User 3',
            user_about='About Demo User 3',
            profile_pic='/path/to/profile3.jpg'
        ),
        User(
            username='DemoUser4',
            email='demo4@example.com',
            password=generate_password_hash('password4'),
            name='Demo User 4',
            user_about='About Demo User 4',
            profile_pic='/path/to/profile4.jpg'
        ),
        User(
            username='DemoUser5',
            email='demo5@example.com',
            password=generate_password_hash('password5'),
            name='Demo User 5',
            user_about='About Demo User 5',
            profile_pic='/path/to/profile5.jpg'
        )
    ]

    db.session.bulk_save_objects(users)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
