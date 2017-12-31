from lib_v2 import blueprints
from flask import jsonify,current_app,request
from werkzeug.utils import secure_filename
import json
import os
import datetime
import subprocess

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def generate_img_url(type, event_id, tournament_id=None,player_id=None):
    timestamp = datetime.datetime.now().strftime("%s")
    if type=="put_edit_event": 
            uploaded_image_url='/img/events/%s/%s.jpg?%s' % (event_id,event_id,timestamp)    
    if type=="put_edit_tournament": 
            uploaded_image_url='/img/events/%s/tournaments/%s.jpg?%s' % (event_id,tournament_id,timestamp)    
    return uploaded_image_url
    

@blueprints.test_blueprint.route('/media_upload',methods=['POST'])
def upload_event_pic():
    # check if the post request has the file part                    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    print "uploading...."    
    if 'image' not in request.files:                                
        print "uploading....uh oh 1"
        return jsonify({})    
    file = request.files['image']            
    if file.filename == '':
        print "uploading....uh oh 2"
        return jsonify({})            
    # if type == "put_edit_event":        
    #     event = tables.Events.query.filter_by(event_id=event_id).first()
    #     save_path=os.path.join('%s/img/events/%s'% (upload_folder,event.event_id), "%s.jpg"%event.event_id)
    #     img_url=generate_img_url(type,event.event_id)
    # if type == "put_edit_tournament":
    #     event = tables.Events.query.filter_by(name=current_app.name).first()
    #     save_path=os.path.join('%s/img/events/%s/tournaments'% (upload_folder,event.event_id), "%s.jpg"%id)                            
    #     img_url=generate_img_url(type,event.event_id,id)
    if file:
        print "uploading....finally"
        filename = secure_filename(file.filename)
        random_file_name = datetime.datetime.now().strftime("%s")+filename
        file.save(upload_folder+"/"+random_file_name)
    return jsonify({'data':"%s"%random_file_name})
