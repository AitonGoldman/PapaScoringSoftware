from flask_restless.helpers import to_dict
from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_required,current_user
import requests
import urllib2
import ssl
import json
import re

def get_ifpa_ranking_via_website(player_name):
    content=requests.get('http://www.ifpapinball.com/ajax/searchplayer.php?search=%s' % player_name).content
    content = content.replace("\n"," ")
    content = content.replace("\r"," ")    
    players = re.findall('player.php\?p=(\d+)\"\>([^\<]+).+?(not ranked|\d+th|\d+nd|\d+st|\d+rd)',content.lower())        
    rank = re.findall('(\d+th|\d+nd|\d+st|\d+rd)', content.lower())    
    actual_ranks = []
    for index,p in enumerate(players):
        #print players[index]
        actual_ranks.append({'wppr_rank':p[2],
                             'player_id':p[0],
                             'first_name':p[1]})
    count = len(players)
    ifpa_results = {'search':actual_ranks}    
    return ifpa_results

@login_required
@blueprints.event_blueprint.route('/ifpa/<player_name>',methods=['GET'])
def route_get_ifpa_ranking(player_name):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE    
    if current_app.event_config['ifpa_api_key']:
        api_key=current_app.event_config['ifpa_api_key']
        search_result_raw = urllib2.urlopen("https://api.ifpapinball.com/v1/player/search?api_key=%s&q=%s" % (api_key,player_name),context=ctx)
        search_results = json.load(search_result_raw)
    else:
        search_results = get_ifpa_ranking_via_website(player_name)
    return jsonify({'data':search_results})
    


