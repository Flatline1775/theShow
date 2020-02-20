from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import mysql.connector

#Bunch of functions to allow me to pull the HTML.  I ripped these off 100%

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
#Setting variables and configuring mySQL connection
page = 1
max_page = 89
cnx = mysql.connector.connect(user='root',password='raspberry',database='theshow')
curA = cnx.cursor(buffered=True)
#Iterate through each page.

while page < max_page:
    raw_html = simple_get('https://mlb19.theshownation.com/community_market?page=' + str(page))
    html = BeautifulSoup(raw_html, 'html.parser')
    first_column = []
    tab = html.find("table",{"class":"items-results-table"})
    rows = tab.findAll('tr')
    #Iterate through all the rows in the rows in the table and write them to a list
    for row in rows[1:]:
        first_column.append(row.findAll('td')[1])
        p_link = re.search('listings\/(.*)">',str(row.findAll('td')[1])).group(1)
        p_name = re.search('">(.*)<\/a>',str(row.findAll('td')[1]),re.DOTALL).group(1)
        p_name = p_name.strip("\n\r")
        p_ovr = re.search('<td>(.*)<img class',str(row.findAll('td')[2]),re.DOTALL).group(1)
        p_ovr = p_ovr.strip("\n\r")
        query1 = 'UPDATE player_19 SET link="' + p_link + '" WHERE name="' + p_name + '" AND ovr=' + str(p_ovr) + ';'
        print(query1)
        curA.execute(query1)
        cnx.commit()
        #print(p_name_test + " " + p_link_test)
        
    page += 1
    
cnx.close()