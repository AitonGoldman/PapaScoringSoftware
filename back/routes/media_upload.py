from blueprints import admin_manage_blueprint
from flask import jsonify,current_app,request
from werkzeug.utils import secure_filename
import json
import os
import datetime

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@admin_manage_blueprint.route('/media_upload/<pic_type>_pic', methods=['POST'])
def upload_file(pic_type):    
    # check if the post request has the file part            
    if 'file' not in request.files:                                
        return jsonify({})        
    file = request.files['file']            
    if file.filename == '':            
        return jsonify({})        
    if file:        
        filename = secure_filename(file.filename)
        random_file_name = datetime.datetime.now().strftime("%s")        
        save_path=os.path.join(current_app.config['UPLOAD_FOLDER'], "%s.jpg"%random_file_name)
        file.save(save_path)
    return jsonify({'data':"%s.jpg"%random_file_name})

