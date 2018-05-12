#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
163MusicFetcher.py

A Python 3 source file.

Usage: Fetch 163 muisc ranking list and download mp3 files.
'''

import time
import os
import requests
import urllib

folder = os.getcwd() + '\\网易云音乐\\'

types = [('http://music.163.com/api/playlist/detail?id=2884035', '网易原创歌曲榜'),
         ('http://music.163.com/api/playlist/detail?id=19723756', '云音乐飙升榜'),
         ('http://music.163.com/api/playlist/detail?id=3778678', '云音乐热歌榜'),
         ('http://music.163.com/api/playlist/detail?id=3779629', '云音乐新歌榜'),
         ('http://music.163.com/api/playlist/detail?id=123415635', '云音乐歌单——【华语】中国风的韵律，中国人的印记'),]

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}


# check #######################################################################
def check_folders():
    if not os.path.isdir(folder):
        os.mkdir(folder)

    for type in types:
        path = folder + '\\' + type[1] + '\\'
        if not os.path.isdir(path):
            os.mkdir(path)
    return


def check_sub_folder(name):
    date = time.strftime("%Y-%m-%d", time.localtime())
    path = folder + name + '\\' + date + "\\"
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def should_download(sub_folder, file_number):
    file_list = os.listdir(sub_folder)
    return len(file_list) != file_number


# clear #######################################################################
def clear():
    os.system('cls')


# menu #######################################################################
def show_menu():
    index = 1
    print('\n\n\t\t欢迎使用网易云音乐批量下载工具\n')
    for type in types:
        print('\t', index, type[1])
        index += 1
    print('\t', '0 退出')


# download #######################################################################
def download(menu):
    url = types[menu][0]
    name = types[menu][1]
    sub_folder = check_sub_folder(name)

    r = requests.get(url, headers=headers)
    arr = r.json()['result']['tracks']  # 共有100首歌
    file_num = len(arr)

    if not should_download(sub_folder, file_num):
        print('\t文件已下载')
        return

    for i in range(file_num):     # 输入要下载的音乐数量
        name = str(i + 1) + ' ' + arr[i]['name'] + '.mp3'
        file_name = sub_folder + name
        # 文件名处理
        if '/' in file_name:
            file_name = file_name.replace('/', '-')

        id = arr[i]['id']
        link = ' http://music.163.com/song/media/outer/url?id=' + str(id)

        # 异常处理
        try:
            urllib.request.urlretrieve(link, file_name)
        except Exception as e:
            print('\t', e)
        else:
            print('\t', name, '下载完成')

    print('\t文件下载完毕')
    return


# main #######################################################################
def main():
    check_folders()
    while True:
        clear()
        show_menu()

        menu = input('\n\t请选择：')
        if not menu.isdigit():
            continue

        menu = int(menu)
        if menu == 0:
            break
        elif menu <= len(types):
            download(menu - 1)
            input('\n\t按回车键返回...')
            continue
        else:
            continue
    return


# start main at last ##########################################################
if __name__ == '__main__':
    main()
