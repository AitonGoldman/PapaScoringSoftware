from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
import urllib2
import ssl
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission, Desk_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity

@login_required
@Desk_permission.require(403)
@admin_manage_blueprint.route('/ifpa/<player_name>',methods=['GET'])
def route_get_ifpa_ranking(player_name):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    #FIXME : this should not be checked in
    api_key="62647a4fcc6e457ea71dde1bc108786c"
    search_result_raw = urllib2.urlopen("https://api.ifpapinball.com/v1/player/search?api_key=%s&q=%s" % (api_key,player_name),context=ctx)
    search_results = json.load(search_result_raw)
    return jsonify({'data':search_results})
