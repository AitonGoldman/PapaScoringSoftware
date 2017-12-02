from lib.serializer import generic
from flask_restless.helpers import to_dict
from lib.flask_lib.single_app_auth import EventCreatorPermission
from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_user_permissions, create_pss_user_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib import orm_factories
from lib.serializer.pss_user import generate_pss_user_to_dict_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from lib.route_decorators.auth_decorators import check_current_user_is_active
from sqlalchemy.orm import joinedload
from lib.PssConfig import PssConfig


@blueprints.pss_admin_event_blueprint.route('/test_global_event_roles',methods=['GET'])
def test_global_event_roles():
    event = current_app.tables.Events.query.first()
    event_role = current_app.tables.EventRoles.query.first()
    users = [pss_user for pss_user in current_app.tables.PssUsers.query.all()]
    for user in users:
        test_class = current_app.tables.TestMapping()
        test_class.pss_user = user
        test_class.event = event
        test_class.event_role = event_role
        user.test_mapping.append(test_class)
    current_app.tables.db_handle.session.commit()
    return jsonify({'users':''})

@blueprints.pss_admin_event_blueprint.route('/test',methods=['GET'])
def test_new_permissions():
    permission = EventCreatorPermission(1)
    if permission.can():
        print "it's okay to go"
    else:
        print "oh no"
    events = [str(event.event_id) for event in current_user.events]
    return jsonify({'user':",".join(events)})

@blueprints.pss_admin_event_blueprint.route('/test_add_permissions',methods=['GET'])
def test_add_new_permissions():    
    event = current_app.tables.Events.query.filter_by(name="poopnormalagain").first()
    current_user.events.append(event)
    current_app.tables.db_handle.session.commit()
    return jsonify({'user':str(current_user)})


