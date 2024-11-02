
# user_service/service.py
from sqlalchemy.orm import sessionmaker
from models import User
from base import engine
from publisher import publish_message

Session = sessionmaker(bind=engine)
session = Session()

def create_user(username, email):
    new_user = User(username=username, email=email)
    session.add(new_user)
    session.commit()
    publish_message('user.created', {'user_id': new_user.id})
