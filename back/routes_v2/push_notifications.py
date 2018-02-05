import time
from pyfcm import FCMNotification
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json

@blueprints.test_blueprint.route('/fcm_tokens/<token>',methods=['GET'])
def get_token(token):        
    #celery_result = send_topic_message.delay(token)    
    print token
    return jsonify({})
