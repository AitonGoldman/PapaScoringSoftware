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
    if 'image' not in request.files:                                        
        return jsonify({})    
    file = request.files['image']            
    if file.filename == '':        
        return jsonify({})            
    if file:        
        filename = secure_filename(file.filename)        
        random_file_name = datetime.datetime.now().strftime("%s")+filename        
        file.save(upload_folder+"/"+random_file_name)
        new_file_path=upload_folder+"/"+random_file_name
        #exiftool -j -Orientation -n 1518227110image.jpg
        #exiftool -Orientation=1 -n "$@"
        #subprocess.call(["exiftool","-Orientation=1", "-n", upload_folder+"/"+random_file_name])
        orientation = subprocess.check_output(["identify", "-format", r"'%[orientation]'",new_file_path])[1:-1]        
        print orientation
        if orientation == "RightTop":            
            subprocess.call(["convert", new_file_path,"-rotate", "90", "%s_rotate"%new_file_path])
        if orientation == "LeftBottom":
            subprocess.call(["convert", new_file_path,"-rotate", "-90", "%s_rotate"%new_file_path])
        subprocess.call(["mv","%s_rotate"%new_file_path,new_file_path])
        subprocess.call(["convert", new_file_path,"-strip", "%s_strip"%new_file_path])
        subprocess.call(["mv","%s_strip"%new_file_path,new_file_path])
        #else:
        #    print "android..."
        #subprocess.call(["convert", save_path,"-crop","200x100+0+0!", "%s_crop"%save_path])
        subprocess.call(["convert", new_file_path,"-resize", "128x128","-define","jpeg:extent=15kb", "%s_resize"%new_file_path])        
        subprocess.call(["mv","%s_resize"%new_file_path,new_file_path])

        
    return jsonify({'data':"%s"%random_file_name})
