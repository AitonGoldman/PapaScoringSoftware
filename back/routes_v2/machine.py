from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
from flask_restless.helpers import to_dict
import json


@blueprints.test_blueprint.route('/machines',methods=['GET'])
def get_machines():            
    #FIXME : need to muck with queues if queue length is changed, or queuing is turned off
    machines_list=[]
    machines = current_app.table_proxy.get_all_machines()
    for machine in machines:        
        machines_list.append(to_dict(machine))        
    return jsonify({'data':machines_list})
