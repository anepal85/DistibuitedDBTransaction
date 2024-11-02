
# inventory_service/service.py
from sqlalchemy.orm import sessionmaker
from models import InventoryItem
from base import engine
from subscriber import subscribe_to

Session = sessionmaker(bind=engine)
session = Session()

@subscribe_to('order.created')
def handle_order_created(message):
    order_data = message['order_data']
    try:
        session.begin()
        for item in order_data['items']:
            inventory_item = session.query(InventoryItem).filter_by(product_id=item['product_id']).first()
            if inventory_item.quantity >= item['quantity']:
                inventory_item.quantity -= item['quantity']
            else:
                raise Exception('Insufficient inventory')
        session.commit()
        # Notify Order Service that inventory update succeeded
        publish_message('inventory.updated', {'order_id': message['order_id'], 'status': 'SUCCESS'})
    except Exception as e:
        session.rollback()
        # Notify Order Service that inventory update failed
        publish_message('inventory.updated', {'order_id': message['order_id'], 'status': 'FAILED'})
