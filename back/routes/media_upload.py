from lib.flask_lib import blueprints
from lib.route_decorators.db_decorators import load_tables
from flask import jsonify,current_app,request
from werkzeug.utils import secure_filename
import json
import os
import datetime
import subprocess

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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
    
@blueprints.event_blueprint.route('/media_upload/jpg_pic',methods=['POST'])
@blueprints.pss_admin_event_blueprint.route('/media_upload/jpg_pic', methods=['POST'])
@load_tables
def upload_file_new(tables):    
    # check if the post request has the file part                    
    upload_folder = current_app.event_config['upload_folder']
    if 'file' not in request.files:                                
        return jsonify({})    
    file = request.files['file']            
    if file.filename == '':            
        return jsonify({})            
    type = request.form.get('type')    
    id = request.form.get('id')        
    if type == "put_edit_event":        
        event = tables.Events.query.filter_by(event_id=id).first()
        save_path=os.path.join('%s/img/events/%s'% (upload_folder,event.event_id), "%s.jpg"%event.event_id)
        img_url=generate_img_url(type,event.event_id)
    if type == "put_edit_tournament":
        event = tables.Events.query.filter_by(name=current_app.name).first()
        save_path=os.path.join('%s/img/events/%s/tournaments'% (upload_folder,event.event_id), "%s.jpg"%id)                            
        img_url=generate_img_url(type,event.event_id,id)
    if file:        
        filename = secure_filename(file.filename)
        random_file_name = datetime.datetime.now().strftime("%s")
        file.save(save_path)
    return jsonify({'data':"%s"%img_url})
