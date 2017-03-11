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
from flask_login import login_required,current_user
from util.permissions import Admin_permission, Desk_permission

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

@admin_manage_blueprint.route('/test/player_in_line_fast', methods=['GET'])
def test_in_line_players_fast():    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    players = {player.player_id:player.to_dict_fast() for player in tables.Player.query.filter_by(pre_reg_paid=False,active=False).all()}
    return jsonify({'data':players})
    # check if the post request has the file part            
    
@admin_manage_blueprint.route('/test/players_with_tickets/<division_id>', methods=['GET'])
def test_players_with_tickets(division_id):    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    players = {player.player_id:player.to_dict_fast() for player in tables.Player.query.all()}
    division = fetch_entity(tables.Division,division_id)
    players_on_machines = {player.player_id:None for player in tables.DivisionMachine.query.filter(tables.Player.player_id is not None).all()}
    if division.team_tournament is True:
        teams_on_machines = {team.team_id:None for team in tables.DivisionMachine.query.filter(tables.Team.team_id is not None).all()}
    
    
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
        if division.team_tournament is True:
            teams_with_tickets = tables.Team.query.join(tables.Token).filter_by(used=False,
                                                                                paid_for=True,
                                                                                voided=False,
                                                                                division_id=division_id).all()
            
    players_with_tickets_dict = {player.player_id:None for player in players_with_tickets}
    if division.team_tournament is True:
        teams_with_tickets_dict = {team.team_id:None for team in teams_with_tickets}
        
    for player_id,player in players.iteritems():
        if player['player_id'] in players_with_tickets_dict:
            player['has_tokens']=True
        if player['player_id'] in players_on_machines:
            player['on_division_machine']=True
        if division.team_tournament is True and 'team_id' in player and player['team_id'] in teams_with_tickets_dict:
            player['has_tokens']=True
        if division.team_tournament is True and 'team_id' in player and player['team_id'] in teams_on_machines:
            player['on_division_machine']=True
        
    return jsonify({'data':players})

@admin_manage_blueprint.route('/test/load_machines', methods=['GET'])
@login_required
@Admin_permission.require(403)
def test_load_machines():    
    # check if the post request has the file part            
    db_util.load_machines_from_json(current_app,False)
    return jsonify({})

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
        #subprocess.call(["convert", save_path,"-resize", "128x128","-define","jpeg:extent=15kb", "%s_resize"%save_path])        
        #subprocess.call(["mv","%s_resize"%save_path,save_path])
    return jsonify({'poop':"%s.jpg"%(random_file_name)})

