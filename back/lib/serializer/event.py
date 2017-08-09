from marshmallow_sqlalchemy import field_for

def generate_events_serializer(app):    
    class events_schema(app.ma.ModelSchema):        
        name = field_for(app.tables.Events, 'name')
        event_id = field_for(app.tables.Events, 'event_id')        
    return events_schema
