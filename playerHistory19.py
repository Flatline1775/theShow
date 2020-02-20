from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import mysql.connector
import time

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
        and content_type is not None
        and content_type.find('html') > -1)
        
def log_error(e):
    print(e)
    
cnx = mysql.connector.connect(user='root',password='raspberry',database='theshow')
curA = cnx.cursor(buffered=True)

query1 = "SELECT player_19.id, player_19.link,(best_sell*.9)-best_buy AS profit FROM player_19 INNER JOIN player_value_19 ON player_19.id = player_value_19.player_id WHERE ((best_sell*.9)-best_buy)>0 AND best_buy > 0 AND link !='' ORDER BY profit DESC LIMIT 10;"
curA.execute(query1)
record = curA.fetchall()

for x in record:
    print(str(x[0]) + " " + str(x[1]) + " " + str(x[2]))

    raw_html = simple_get('https://mlb19.theshownation.com/community_market/listings/' + str(x[1]))
    html = BeautifulSoup(raw_html, 'html.parser')
    tab = html.find("table",{"id":"table-completed-orders"})
    rows = tab.findAll('tr')
    #print(rows)

    for row in rows[1:]:
        try:
            p_value = re.search('png"\/>\n(.*)\n<\/td>',str(row.findAll('td')[0])).group(1)
            p_time =  re.search('<td>(.*)PST',str(row.findAll('td')[1])).group(1)
            
            p_value = p_value.replace(",","")
            
            s_time = time.strptime(p_time, "%m/%d/%Y %I:%M%p ")
            f_time = str(s_time.tm_year)+"-"+str(s_time.tm_mon).zfill(2)+"-"+str(s_time.tm_mday).zfill(2)+" "+str(s_time.tm_hour).zfill(2)+":"+str(s_time.tm_min).zfill(2)+":00"
            
            #print(p_value)
            
            query2 = "INSERT INTO sales_19 (player_id, amt, dt) VALUES (" + str(x[0]) + "," + p_value + ",'" + f_time + "')"
            curA.execute(query2)
            cnx.commit()
            print(query2)
        except:
            fakething=1
cnx.close()