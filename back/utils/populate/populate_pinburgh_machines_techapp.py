import os,sys
import csv
import json

machines={1:[],2:[],3:[],4:[]}
with open('machines.csv', 'rb') as csvfile:
    machinereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in machinereader:
        for index,machine in enumerate(row[2:]):
            try:
                machine_id = int(machine[-4:])
                machine_name = machine[:-7]                
                #machines[index+1].append({'machine_location':row[1],'machine_four_digit_id':machine_id,'machine_name':machine_name,'machine_era_type':index+1})
	        f= open("/tmp/data/machine_%s.json" % machine_id,"w+")
                f.write(json.dumps({'body':{'machine_location':'bank %s' % row[1],'machine_four_digit_id':machine_id,'machine_name':machine_name,'machine_era_type':index+1}}))
                f.close()
                
            except Exception as a:
                print "uh oh - %s has no id" % machine                
                pass
#print machines

with open('backup_machines.csv', 'rb') as csvfile:
    machinereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in machinereader:
        for index,machine in enumerate(row[2:]):
            try:
                machine_id = int(machine[-4:])
                machine_name = machine[:-7]                
                #machines[index+1].append({'machine_location':row[1],'machine_four_digit_id':machine_id,'machine_name':machine_name,'machine_era_type':index+1})
	        f= open("/tmp/backup_data/machine_%s.json" % machine_id,"w+")
                f.write(json.dumps({'body':{'backup_machine':True,'machine_location':'bank %s' % row[1],'machine_four_digit_id':machine_id,'machine_name':machine_name,'machine_era_type':index+1}}))
                f.close()
                
            except Exception as a:
                print "uh oh - %s has no id" % machine                
                pass



# ranked_finals_player_dicts=[]

# def build_finals_player_dict(finals_player_id,player_name,seed):
#     return {'finals_player_id':finals_player_id,
#             'player_name':player_name,
#             'seed_rank':seed,
#             'present':True}

# for player in players:
#     db_player = app.table_proxy.create_player(player[0]," ",commit=True)
#     finals_player = app.table_proxy.create_finals_player(event_id,db_player.player_id,tournament_id,player[1],commit=True)
#     ranked_finals_player_dicts.append(build_finals_player_dict(finals_player.finals_player_id,player[0],player[1]))

# payload_string=json.dumps({'description':"placeholder text","data":ranked_finals_player_dicts})
# print payload_string
