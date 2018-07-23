def deserialize_json(model,input_data,app,allow_foreign_keys=False):
    for c in model.__table__.columns:        
        if c.primary_key:
            continue            
        if allow_foreign_keys is False and len(c.foreign_keys) > 0:
            continue            
        if c.name in input_data:
            setattr(model,c.name,input_data[c.name])
        #elif c.name not in input_data and isinstance(c.type,app.tables.db_handle.Boolean):
        #    setattr(model,c.name,None)
