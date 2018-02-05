from celery import Celery
import time
from pyfcm import FCMNotification
import os

celery_instance = Celery('tasks', broker='pyamqp://guest@localhost//')
fcm_api_key=os.getenv('FCM_API_KEY')
@celery_instance.task
def send_topic_message(msg):    
    push_service = FCMNotification(api_key=fcm_api_key)    
    message_title = "Papa Scoring Software"
    message_body = "Hi %s, your customized news for today is ready" % msg
    #time.sleep(10)
    #result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)    
    result = push_service.notify_topic_subscribers(topic_name="all", message_body=message_body, message_title=message_title)    
    return None

    
