from blueprints import admin_manage_blueprint
from flask import jsonify,current_app,request
from werkzeug.utils import secure_filename
import json
import os
import subprocess
from util import db_util
from routes.utils import fetch_entity
import datetime
import time

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@admin_manage_blueprint.route('/test/lock_row', methods=['GET'])
def test_lock_queue():    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    #queue = db.session.query(tables.Queue).with_for_update().filter_by(queue_id=3687).first()
    queue = tables.Queue.query.with_for_update().filter_by(division_machine_id=11).all()    
    #players = {player.player_id:player.to_dict_fast() for player in tables.Player.query.all() if player.active is True}
    queue[0].player_id=89
    db.session.commit()
    queue_list = []
    division_machine = fetch_entity(tables.DivisionMachine,11)
    for queue in division_machine.queue:
        queue_list.append(queue.to_dict_simple())
    return jsonify({'data':queue_list})
    # check if the post request has the file part            

@admin_manage_blueprint.route('/test/player_fast', methods=['GET'])
def test_players_fast():    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    players = {player.player_id:player.to_dict_fast() for player in tables.Player.query.filter_by(active=True).all()}
    return jsonify({'data':players})
    # check if the post request has the file part            

@admin_manage_blueprint.route('/test/player_prereg_fast', methods=['GET'])
def test_prereg_players_fast():    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    players = {player.player_id:player.to_dict_fast() for player in tables.Player.query.filter_by(pre_reg_paid=True,active=False).all()}
    return jsonify({'data':players})
    # check if the post request has the file part            
    
@admin_manage_blueprint.route('/test/players_with_tickets/<division_id>', methods=['GET'])
def test_players_with_tickets(division_id):    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    players = {player.player_id:player.to_dict_fast() for player in tables.Player.query.all()}
    division = fetch_entity(tables.Division,division_id)         
    if division.meta_division_id:
        players_with_tickets = tables.Player.query.filter_by(active=True).join(tables.Token).filter_by(used=False,
                                                                                paid_for=True,
                                                                                voided=False,
                                                                                metadivision_id=division.meta_division_id).all()        
    else:
        players_with_tickets = tables.Player.query.filter_by(active=True).join(tables.Token).filter_by(used=False,
                                                                                paid_for=True,
                                                                                voided=False,
                                                                                division_id=division_id).all()
    players_with_tickets_dict = {player.player_id:player.to_dict_fast() for player in players_with_tickets}
    for player_id,player in players.iteritems():
        if player['player_id'] in players_with_tickets_dict:
            player['has_tokens']=True
    return jsonify({'data':players})

    # db = db_util.app_db_handle(current_app)
    # tables = db_util.app_db_tables(current_app)
    # division = fetch_entity(tables.Division,division_id)     
    # if division.meta_division_id:
    #     players_with_tickets = tables.Player.query.filter_by(active=True).join(tables.Token).filter_by(used=False,
    #                                                                             paid_for=True,
    #                                                                             voided=False,
    #                                                                             metadivision_id=division.meta_division_id).all()        
    # else:
    #     players_with_tickets = tables.Player.query.filter_by(active=True).join(tables.Token).filter_by(used=False,
    #                                                                             paid_for=True,
    #                                                                             voided=False,
    #                                                                             division_id=division_id).all()
    # return jsonify({'data':{player.player_id:player.to_dict_fast() for player in players_with_tickets}})    
    # check if the post request has the file part            

@admin_manage_blueprint.route('/test/media_upload', methods=['POST'])
def test_upload_file():    
    # check if the post request has the file part            
    if 'file' not in request.files:                                
        return jsonify({})        
    file = request.files['file']            
    if file.filename == '':            
        return jsonify({})        
    if file:                        
        filename = secure_filename(file.filename)                        
        #save_path=os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        random_file_name = datetime.datetime.now().strftime("%s")
        save_path=os.path.join(current_app.config['UPLOAD_FOLDER'],"%s.jpg"%random_file_name)
        file.save(save_path)
        file.close()
        #convert /var/www/html/pics/player_1.jpg  -resize 128x128  /var/www/html/pics/resize_player_1.jpg
        subprocess.call(["convert", save_path,"-resize", "128x128","-define","jpeg:extent=15kb", "%s_resize"%save_path])        
        subprocess.call(["mv","%s_resize"%save_path,save_path])
    return jsonify({'poop':"%s.jpg"%(random_file_name)})

