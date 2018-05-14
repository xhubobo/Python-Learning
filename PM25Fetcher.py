#!/usr/bin/env/ python
# -*- coding: utf-8 -*-

r'''
获取PM2.5信息
'''

import threading
import urllib.request
from time import ctime
from bs4 import BeautifulSoup

Url_Base = 'http://www.pm25.com/'
Url_Postfix = '.html'


def get_pm25(city_name):
    site = Url_Base + city_name + Url_Postfix
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, "html.parser")

    city = soup.find(class_ = 'bi_loaction_city') # 城市名称
    aqi = soup.find("a", {"class", "bi_aqiarea_num"}) # AQI指数
    quality = soup.select(".bi_aqiarea_right span") # 空气质量等级
    result = soup.find("div", class_ = 'bi_aqiarea_bottom') #空气质量描述

    print(city.text + u'AQI指数：' + aqi.text + u'\n空气质量：' + quality[0].text + result.text)
    print('*'*20, ctime(), '*'*20, '\n')


# 单线程
def single_thread():
    print('Single thread start:', ctime())
    get_pm25('xuchang')
    get_pm25('zhengzhou')


# 多线程
def multi_thread():
    print('Multi threads start:', ctime())
    threads = []
    t1 = threading.Thread(target=get_pm25, args=('luoyang',))
    threads.append(t1)
    t2 = threading.Thread(target=get_pm25, args=('kaifeng',))
    threads.append(t2)

    for t in threads:
        t.start()


if __name__ == '__main__':
    single_thread()
    print('\n' * 2)
    multi_thread()
    # get_pm25('xuchang')
