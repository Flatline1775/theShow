from requests import get
import json
from pprint import pprint
import mysql.connector
import datetime

page = 1
max_page = 88
last_count = 1

cnx = mysql.connector.connect(user='root',password='raspberry',database='theshow')
curA = cnx.cursor(buffered=True)
queryDel = "TRUNCATE TABLE player_value_19"
curA.execute(queryDel)
cnx.commit()
print("Table truncated.")
while page < max_page:
    url = 'https://mlb19.theshownation.com/apis/listings.json?type=MLB_Card&page=' + str(page)
    cards = get(url).json()
    for index, x in enumerate(cards["listings"],last_count):
        query1 = "SELECT id FROM player_19 WHERE name = \""+str(x["name"])+"\" AND rel_id = " + str(last_count)
        #print(query1)
        #print(index)
        curA.execute(query1)
        i = 0
        e_check = 0
        while i < 1:
            try: 
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                record=curA.fetchall()
                query2 = "INSERT INTO player_value_19 (player_id, best_sell, best_buy, datetime) VALUES (" + str(record[0][0]) + "," + str(x["best_sell_price"]) + "," + str(x["best_buy_price"]) + ",'" + str(ts) + "')"
                #print(query2)
                curA.execute(query2)
                print (x["name"] + " record submitted.")
                last_count += 1
                cnx.commit()
                #print(last_count)
                i = 1
            except:
                e_check += 1
                if e_check < 25:
                    last_count += 1
                    query1 = "SELECT id FROM player_19 WHERE name = \""+str(x["name"])+"\" AND rel_id = " + str(last_count)
                    #print("Exception: " + query1)
                    curA.execute(query1)
                else:
                    i = 1
                    e_check = 0
                    last_count = last_count - 25
    page += 1



cnx.close()