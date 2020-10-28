import urllib
from urllib import request

def string_convert_to_hex(string):

    hex_string = ""

    for i in string:
        hex_string += hex(ord(i))

    return '0x' + hex_string.replace('0x', '')  # 将dbname变成16进制

def hex_list_convert_to_dec_list(hex_list):

    for i in range(0, len(hex_list)):

        hex_list[i] = int(hex_list[i], 16)

    return hex_list


def ascii_list_convert_to_hex_list(ascii_list):

    for i in range(0, len(ascii_list)):

        ascii_list[i] = hex(int(ascii_list[i]))

    return ascii_list


def ascii_list_convert_to_string(ascii_list):

    for i in range(0, len(ascii_list)):

        ascii_list[i] = chr(int(ascii_list[i]))

    return ascii_list


def url_request(url,cookie):

    url_response = urllib.request.Request(url)

    if (cookie != False):
        url_response.add_header('Cookie', cookie)

    return request.urlopen(url_response).read()



if __name__ == "__main__":

    print('admin')