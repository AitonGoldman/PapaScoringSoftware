import requests
import urllib2
import urllib
import ssl
import json
import re
import os
import sys
import time

def get_ifpa_ranking(player_name):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE    
    
    api_key=""
    player_name_clean = player_name.replace(' ',r'%20').replace("'",'')
    search_result_raw = urllib2.urlopen("https://api.ifpapinball.com/v1/player/search?api_key=%s&q=%s" % (api_key,player_name_clean),context=ctx)
    search_results = json.load(search_result_raw)            
    if len(search_results['search'])==0:
        return ""
    if len(search_results['search'])==1:
        return search_results['search'][0]['player_id']
    if len(search_results['search']) > 1:
        print "too many results for %s" % player_name
    
    
    
f = open(sys.argv[1], 'r')
json_results = f.read()
f.close()
results = json.loads(json_results)
ranked_results =  results['data']['ranked_player_list']['1']
current_rank = 1
for result in ranked_results:
    if int(sys.argv[2])<current_rank:
        time.sleep(2)
        ifpa=get_ifpa_ranking(result[1]['player_name'])
    else:
        ifpa=" "
    print "%s,%s,%s" % (result[0]+1,result[1]['player_name'],ifpa)
    
    current_rank=current_rank+1
