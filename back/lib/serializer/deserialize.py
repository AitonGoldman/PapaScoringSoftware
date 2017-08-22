def deserialize_json(model,input_data,app):
    for c in model.__table__.columns:        
        if len(c.foreign_keys) > 0 or c.primary_key:
            continue
        if c.name in input_data:
            setattr(model,c.name,input_data[c.name])
        elif c.name not in input_data and isinstance(c.type,app.tables.db_handle.Boolean):
            setattr(model,c.name,None)
