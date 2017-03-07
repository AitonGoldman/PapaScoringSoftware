from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission, Desk_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity
import os
from orm_creation import create_player,create_user,RolesEnum
import random
import subprocess

@admin_manage_blueprint.route('/player/division_id/<division_id>',methods=['GET'])
def route_get_players_for_division_with_tickets(division_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    players = {player.player_id:player.to_dict_simple() for player in tables.Player.query.filter_by(linked_division_id=division_id).all()}
    return jsonify({'data':players})

@admin_manage_blueprint.route('/player',methods=['GET'])
def route_get_players():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    players = {player.player_id:player.to_dict_simple() for player in tables.Player.query.all()}
    return jsonify({'data':players})

@admin_manage_blueprint.route('/player/<player_id>',methods=['GET'])
def route_get_player(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    player = fetch_entity(tables.Player,player_id)     
    return jsonify({'data':player.to_dict_simple()})


@admin_manage_blueprint.route('/player/<player_id>',methods=['PUT'])
@login_required
@Desk_permission.require(403)
def route_edit_player(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    input_data = json.loads(request.data)
    player = fetch_entity(tables.Player,player_id)     
    if 'first_name' in input_data:
        player.first_name = input_data['first_name']
    if 'last_name' in input_data:
        player.last_name = input_data['last_name']
    if 'email_address' in input_data:
        player.email_address = input_data['email_address']
    if 'ifpa_ranking' in input_data:
        player.ifpa_ranking = input_data['ifpa_ranking']
    if 'active' in input_data:
        player.active=input_data['active']
    if 'linked_division_id' in input_data and input_data['linked_division_id'] is not None:
        # Get all scores from old division
        # void all those scores
        # change linked_division_id
        if int(input_data['linked_division_id']) != player.linked_division_id:
            entries = tables.Entry.query.filter_by(player_id=player_id,division_id=player.linked_division_id).all()
            for entry in entries:
                entry.voided=True
        player.linked_division_id = input_data['linked_division_id']
    if 'pic_file' in input_data:
        player.has_pic=True
        save_path = "%s/%s"%(current_app.config['UPLOAD_FOLDER'],input_data['pic_file'])
        subprocess.call(["convert", save_path,"-resize", "128x128","-define","jpeg:extent=15kb", "%s_resize"%save_path])
        subprocess.call(["mv","%s_resize"%save_path,save_path])        
        os.system('mv %s/%s /var/www/html/pics/player_%s.jpg' % (current_app.config['UPLOAD_FOLDER'],input_data['pic_file'],player.player_id))        
        
    db.session.commit()                        
    return jsonify({'data':player.to_dict_simple()})        

@admin_manage_blueprint.route('/player/<player_id>/pin',methods=['GET'])
@login_required
@Desk_permission.require(403)
def route_get_player_pin(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    player = fetch_entity(tables.Player,player_id)     
    db.session.commit()                        
    return jsonify({'data':player.pin})        

@admin_manage_blueprint.route('/player',methods=['POST'])
@login_required
@Desk_permission.require(403)
def route_add_player():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    input_data = json.loads(request.data)
    for key in ['first_name','last_name','ifpa_ranking']:
        if key not in input_data:
            raise BadRequest("You did not specify a first name and/or a last name and/or a ifpa ranking")        
    player = tables.Player.query.filter_by(first_name=input_data['first_name'],last_name=input_data['last_name']).first()
    if player is not None:
        raise Conflict('Duplicate player')
    new_player = create_player(current_app,input_data)
    db.session.commit()
    new_player_dict = new_player.to_dict_simple()
    new_player_dict['pin']=new_player.pin
    return jsonify({'data':new_player_dict})

@admin_manage_blueprint.route('/pre_reg_player',methods=['POST'])
def route_add_prereg_player():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    input_data = json.loads(request.data)
    for key in ['first_name','last_name','ifpa_ranking']:
        if key not in input_data:
            raise BadRequest("You did not specify a first name and/or a last name and/or a ifpa ranking")        
    player = tables.Player.query.filter_by(first_name=input_data['first_name'],last_name=input_data['last_name']).first()
    if player is not None:
        if player.active is True:
            raise Conflict('Duplicate player')
        if player.active is False and player.pre_reg_paid is True:
            raise Conflict('Duplicate player')            
    input_data['active']=False
    new_player = create_player(current_app,input_data)
    db.session.commit()
    new_player_dict = new_player.to_dict_simple()
    new_player_dict['pin']=new_player.pin
    return jsonify({'data':new_player_dict})

