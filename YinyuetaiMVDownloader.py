#!/usr/bin/env python
# -*- coding: utf-8 -*-

r'''
YinyuetaiMVDownloader.py

A MV downloader form http://www.yinyuetai.com

Usage: Download MV from yinyuetai.
'''

import requests
import re
import os
from urllib import request

Url_Base = 'http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId='
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
reg = r'http://\w*?\.yinyuetai\.com/uploads/videos/common/.*?(?=&br)'
folder = os.getcwd() + '\\音悦台MV\\'
time_out = 30


class MVUrlInfo(object):
    'MV Url信息'
    url = ''
    des = ''
    tag = ''
    tag_weight = 0

    def __init__(self, url, des, tag, tag_weight):
        self.url = url
        self.des = des
        self.tag = tag
        self.tag_weight = tag_weight


def check_folders():
    if not os.path.isdir(folder):
        os.mkdir(folder)
    return


def get_local_file(mv_id, mv_url, mv_tag):
    local = folder + mv_id + '_' + mv_tag + '.flv'

    begin = mv_url.rfind('.')
    end = mv_url.rfind('?')

    if begin == -1 or end == -1:
        return local

    local = folder + mv_id + '_' + mv_tag + mv_url[begin:end]
    return local


MV_url_base_hc = 'http://hc.yinyuetai.com/' # VIP专享MV
MV_url_base_hd = 'http://hd.yinyuetai.com/' # 超清MV
MV_url_base_he = 'http://he.yinyuetai.com/' # 高清MV
MV_url_base_sh = 'http://sh.yinyuetai.com/' # 流畅MV


def get_mv_url(find_list):
    mv_url = ''
    mv_tag = ''
    list_info = []

    # print(find_list[len(find_list) - 1])

    # 音悦台的视频类型弄反了
    for url in find_list:
        if MV_url_base_hd in url:
            info = MVUrlInfo(url, '流畅MV', 'sh', 3)
        elif MV_url_base_he in url:
            info = MVUrlInfo(url, '高清MV', 'he', 2)
        elif MV_url_base_sh in url:
            info = MVUrlInfo(url, '超清MV', 'hd', 1)
        else:
            continue
        # print(info.des)
        list_info.append(info)

    if len(list_info) == 0:
        print('\t没有可用的MV')
        return mv_url, mv_tag

    list_info.sort(key=lambda x: x.tag_weight)

    while True:
        print('\n\tMV类型：')
        for i in range(len(list_info)):
            print('\t', i + 1, list_info[i].des)
        print('\t', '0 取消\n')

        menu = input('\n\t请选择：')
        if not menu.isdigit():
            continue

        menu = int(menu)
        if menu == 0:
            print('\t取消下载')
            break
        elif menu <= len(list_info):
            mv_url = list_info[menu - 1].url
            mv_tag = list_info[menu - 1].tag
            print('\t已选择', list_info[menu - 1].des, '\n')
            break
        else:
            continue

    return mv_url, mv_tag


def download_mv(mv_id): # 3210045
    url = Url_Base + mv_id
    r = requests.get(url, headers=headers)
    html = r.text

    pattern = re.compile(reg)
    find_list = re.findall(pattern, html)  # 找到MV所有版本的下载链接
    find_list_len = len(find_list)

    # for i in find_list:
    #   print(i)

    if find_list_len > 0:
        mv_url, mv_tag = get_mv_url(find_list)
        if not mv_url or len(mv_url) == 0:
            return

        local = get_local_file(mv_id, mv_url, mv_tag)

        if os.path.exists(local):
            print('\t文件已下载')
            return

        try:
            print('\n\t正在下载中，请稍后...')
            request.urlretrieve(mv_url, local)
            print('\t文件下载成功')
        except IOError:
            print('\t文件下载失败')
    else:
        print('\n\t无效的MV编号', mv_id)


def main():
    check_folders()
    while True:
        os.system('cls')
        print('\n\n\t\t欢迎使用音悦台MV下载工具\n')
        mv_id = input('\t请输入MV ID(0退出)：')

        if mv_id == '0':
            break
        else:
            download_mv(mv_id)
            input('\n\t按回车键返回...')
            continue
    input('\n\t谢谢使用！(回车键退出)')
    return


if __name__ == '__main__':
    main()
