from flask import Flask
from lib_v2.PssConfig  import PssConfig
from lib_v2.TableProxy import TableProxy
import os,sys
from lib_v2 import bootstrap,roles_constants
import csv
from lib_v2 import app_build
import json


app=app_build.build_app(Flask('pss'))

if len(sys.argv) < 2:
    print "args : tournament_id event_id"
    sys.exit(1)
    
tournament_id=sys.argv[1]
event_id=sys.argv[1]

players=[]
with open('players.csv', 'rb') as csvfile:
    playereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in playereader:
        players.append(row)

ranked_finals_player_dicts=[]

def build_finals_player_dict(finals_player_id,player_name,seed):
    return {'finals_player_id':finals_player_id,
            'player_name':player_name,
            'seed_rank':seed,
            'present':True}

for player in players:
    db_player = app.table_proxy.create_player(player[0]," ",commit=True)
    finals_player = app.table_proxy.create_finals_player(event_id,db_player.player_id,tournament_id,player[1],commit=True)
    ranked_finals_player_dicts.append(build_finals_player_dict(finals_player.finals_player_id,player[0],player[1]))

payload_string=json.dumps({'description':"placeholder text","data":ranked_finals_player_dicts})
print payload_string
