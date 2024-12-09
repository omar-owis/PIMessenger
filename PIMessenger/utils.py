from flask import request

def upload_items(model, data_field, primary_key, db_session):
    items = request.get_json().get(data_field, [])
    db_items = db_session.query(model).all()
    db_field_values = [getattr(item, primary_key) for item in db_items]
    incoming_field_values = [item[primary_key] for item in items]
    
    # delete items from db that are not in the incoming data
    model.query.filter(getattr(model, primary_key).notin_(incoming_field_values)).delete(synchronize_session=False)
    
    # update or add items
    for item in items:
        db_item = model.query.get(item[primary_key])
        if db_item:
            # if the item exists, update fields
            for field, value in item.items():
                if getattr(db_item, field) != value:
                    setattr(db_item, field, value)
        else:
            # if the item does not exist, create a new record
            db_session.add(model(**item))
    
    db_session.commit()
