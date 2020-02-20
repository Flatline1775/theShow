from requests import get
import json
from pprint import pprint
import mysql.connector

page = 1
max_page = 99 #This should be set so that all cards get pulled in.
last_count = 1 #This needs to stay at 1.  It sets the value for rel_id which is probably useless if I can assume player and name and ovr will always be unique.

cnx = mysql.connector.connect(user='root',password='raspberry',database='theshow')
curA = cnx.cursor(buffered=True)
#Pulls the entire list of cards from The Show 19.  Validates against a composite key of player name and ovr with the assumption that SDS will never release a player with the same ovr twice.
while page < max_page:
    url = 'https://mlb19.theshownation.com/apis/items.json?type=MLB_Card&page=' + str(page)
    cards = get(url).json()
    sql_col = ('rel_id','name','rarity','team','ovr','age','bat_hand','throw_hand','stamina','pitching_clutch','hits_per_bf','k_per_bf','bb_per_bf','hr_per_bf','pitch_velocity','pitch_control','pitch_movement','contact_left','contact_right','power_left','power_right','plate_vision','plate_discipline','batting_clutch','bunting_ability','drag_bunting_ability','hitting_durability','fielding_ability','arm_strength','arm_accuracy','reaction_time','blocking','speed','baserunning_ability','baserunning_aggression')
    for index, x in enumerate(cards["listings"],last_count):
        py_col = ('"'+str(x["name"])+'"',"'"+str(x["rarity"])+"'","'"+str(x["team"])+"'",str(x["ovr"]),str(x["age"]),"'"+str(x["bat_hand"])+"'","'"+str(x["throw_hand"])+"'",str(x["stamina"]),str(x["pitching_clutch"]),str(x["hits_per_bf"]),str(x["k_per_bf"]),str(x["bb_per_bf"]),str(x["hr_per_bf"]),str(x["pitch_velocity"]),str(x["pitch_control"]),str(x["pitch_movement"]),str(x["contact_left"]),str(x["contact_right"]),str(x["power_left"]),str(x["power_right"]),str(x["plate_vision"]),str(x["plate_discipline"]),str(x["batting_clutch"]),str(x["bunting_ability"]),str(x["drag_bunting_ability"]),str(x["hitting_durability"]),str(x["fielding_ability"]),str(x["arm_strength"]),str(x["arm_accuracy"]),str(x["reaction_time"]),str(x["blocking"]),str(x["speed"]),str(x["baserunning_ability"]),str(x["baserunning_aggression"]))
        query = "INSERT INTO player_19 (" + ','.join(sql_col) + ") VALUES(" + str(index) + ',' + ','.join(py_col) + ") ON DUPLICATE KEY UPDATE rel_id = " + str(index)
        print(query)
        last_count += 1
        curA.execute(query)
    page += 1

cnx.commit()
cnx.close()