from result import Ok, Err
import urllib, time, threading
from urllib import request
from data import glovar, glofun
from concurrent.futures import ThreadPoolExecutor
import time

# def myFun(args1,args2,args3):
#
#     print(args1)
#     print(args2)
#     print(args3)
#
# # Now we can use *args or **kwargs to
# # pass arguments to this function :
# args = ("Geeks", "for", "Geeks")
# #args='geeks0'
# args1='geeks1'
#
# #args2= ("Geeks2", "for2", "Geeks2")
#
# myFun(args)
#
# a = [1, 2, 3]
# b = [4, 5, 6]
# c = [4, 5, 6, 7, 8]
# zipped = zip(a, b)  # 返回一个对象
#
#   # list() 转换为列表
# print(list(zipped))
# print(list(zip(a, c)))
#  # 元素个数与最短的列表一致
# #[(1, 4), (2, 5), (3, 6)]
#
# a1, a2 = zip(*zip(a, b))  # 与 zip 相反，zip(*) 可理解为解压，返回二维矩阵式
#
# print(list(a1))
#
# #[1, 2, 3]
# print(list(a2))
#
# #[4, 5, 6]
#
# for args in zip(*zip(a, b)):
#  print(args)
#  print(1)

# from concurrent.futures import ThreadPoolExecutor
# import time
#
#
# # 参数times用来模拟网络请求的时间
# def get_html(times):
#     time.sleep(times)
#     print("get page {}s finished".format(times))
#     return times
#
#
# executor = ThreadPoolExecutor(max_workers=2)
# urls = [3, 2, 4]  # 并不是真的url
#
# for data in executor.map(get_html, urls):
#     print("in main: get page {}s success".format(data))

import threading

# 创建全局ThreadLocal对象:
local_school = threading.local()


def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))


def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()


t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Bob',), name='Thread-B')

t1.start()
t2.start()
t1.join()
t2.join()