# order_service/service.py
from sqlalchemy.orm import sessionmaker
from models import Order
from base import engine
from subscriber import subscribe_to
from publisher import publish_message

Session = sessionmaker(bind=engine)
session = Session()

@subscribe_to('user.created')
def handle_user_created(message):
    user_id = message['user_id']
    # Logic to handle new user creation if necessary

def create_order(user_id, order_data):
    new_order = Order(user_id=user_id, status='PENDING')
    session.add(new_order)
    session.commit()
    publish_message('order.created', {'order_id': new_order.id, 'order_data': order_data})

@subscribe_to('inventory.updated')
def handle_inventory_updated(message):
    order_id = message['order_id']
    status = message['status']
    order = session.query(Order).filter_by(id=order_id).first()
    if status == 'SUCCESS':
        order.status = 'CONFIRMED'
        session.commit()
    else:
        session.delete(order)
        session.commit()