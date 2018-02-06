import time
from pyfcm import FCMNotification
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json

@blueprints.test_blueprint.route('/fcm_tokens/player/<int:player_id>',methods=['PUT'])
def get_token(player_id):        
    #celery_result = send_topic_message.delay(token)    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    token = input_data['token']    
    return jsonify({})
