import urllib
from urllib import request

def hex_convert(string):

    hex_string = ""

    for i in string:
        hex_string += hex(ord(i))

    return '0x' + hex_string.replace('0x', '')  # 将dbname变成16进制

def url_request(url,cookie):

    url_response = urllib.request.Request(url)

    if (cookie != False):
        url_response.add_header('Cookie', cookie)

    return request.urlopen(url_response).read()


# count = 0
#
# def get_name_bylength(response_length,url_read_length,k):
#
#     if k == 1:
#
#         if response_length < url_read_length:
#
#             response_length = url_read_length
#
#             coname = chr(int(j))
#
#
#     if (response_length - url_read_length) < 50:
#
#         if j == '0':
#
#             coname_list.append(coname)
#
#             print(coname)
#
#             coname = ""
#
#             break
#
#         coname += chr(int(j))
#
#         print(coname)


if __name__ == "__main__":

    print(hex_convert('admin'))