# -*- coding: utf-8 -*-

from datetime import datetime
import os
from os import path
import re
import time
import traceback
import sys

from bs4 import BeautifulSoup
from lxml import etree
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import pymysql

# 保存路径
parentFolder = os.path.join(os.getcwd(), 'previews')
# 文件限制1M
size_limit = 1024.0 * 1024.0
# 请求 header
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br'}

# 更新数据库
def updateDatabase(name, date, preview_url, detail_url, size):
    # 动态选择数据库服务器地址（如果在 server 端运行，没必要走外网地址）
    ip_address = ''
    if sys.platform.startswith('win'):
        ip_address = '112.125.25.230'
    elif sys.platform.startswith('linux'):
        ip_address = '127.0.0.1'
    db = pymysql.connect(ip_address,'klq26','abc123!@#==','video_unique')
    cursor = db.cursor()
    sql = r"INSERT INTO pornlib(name, date, preview_url, detail_url, size) VALUES ('{0}', '{1}', '{2}', '{3}', {4})".format(name, date, preview_url, detail_url, size)
    # print("[SQL] {0}".format(sql))
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

# 判断是否已经看过了（不管是下过留下 or 下过删除了）
def isAlreadyViewed(detail_url):
    ip_address = ''
    if sys.platform.startswith('win'):
        ip_address = '112.125.25.230'
    elif sys.platform.startswith('linux'):
        ip_address = '127.0.0.1'
    db = pymysql.connect(ip_address,'klq26','abc123!@#==','video_unique')
    cursor = db.cursor()
    sql = r"SELECT detail_url FROM pornlib WHERE detail_url = '{0}'".format(detail_url)
    # print("[SQL] {0}".format(sql))
    cursor.execute(sql)
    detail_list = [x[0] for x in list(cursor.fetchall())]
    # print(preview_list)
    cursor.close()
    db.close()
    
    if len(detail_list) > 0:
        return True
    else:
        return False

def fetchPreviewVideos():
    # host
    host = u'https://www.pornlib.com'
    # 分类
    categories = ['amateur','blonde','bbw','doggystyle','interracial','japanese','asian','milf','mature','hardcore','gangbang','cumshot','lingerie','old-young','outdoor','public','threesome']
    cate_index = 0
    cate_pages = 2
    cate_count = len(categories) * cate_pages
    for category in categories:
        # 每天取前 2 页
        for i in range(1, cate_pages + 1):
            cate_index += 1
            url = u'{0}/{1}/{2}'.format(host, category, i)
            print(url)
            folderName = u'page{0}'.format(i)
            print(u'category: {0} {1} {2} / {3} {4}%'.format(category, folderName, cate_index, cate_count, round(float(cate_index)/cate_count * 100, 2)))
            video_idx = 1
            try:
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                # 请求当前列表页
                response = requests.get(url, headers=header, verify=False)
                if response.status_code == 200 and len(response.text) > 0:
                    soup = BeautifulSoup(response.text, 'lxml')
                    elements = soup.find_all(
                        'div', attrs={'class': 'thumb wrap-better-content'})
                    totalCount = len(elements)
                    count = 0
                    if totalCount > 0:
                        dateString = time.strftime(
                            '%Y%m%d', time.localtime(time.time()))
                        folderPath = os.path.join(parentFolder, dateString, category, folderName)
                        if not os.path.exists(folderPath):
                            print('create folder')
                            os.makedirs(folderPath)
                        # 遍历当前列表页中的每一个视频卡片 element
                        for element in elements:
                            img = element.find_all('img')[0]
                            a = element.find_all('a')[0]
                            hyperlink = 'https://www.pornlib.com' + a.get('href')
                            # 视频预览图地址在 img 元素内
                            webmVideoUrl = img.get('data-webm')
                            if webmVideoUrl.startswith('//'):
                                webmVideoUrl = webmVideoUrl.replace('//', 'http://')
                            videoTitle = '{0}_{1}'.format(str(video_idx).zfill(3),img.get('alt'))
                            # print(videoTitle,webmVideoUrl,os.path.splitext(webmVideoUrl)[1],hyperlink)
                            if isAlreadyViewed(hyperlink):
                                print('[Skip] {0} duplicated. Skip.'.format(videoTitle))
                                count += 1
                                continue
                            # 先检查是否已经下载过
                            videoFilePath = os.path.join(
                                folderPath, '{0}.mp4'.format(videoTitle))                            
                            # 下载保存视频
                            try:
                                response = requests.get(webmVideoUrl, headers=header, stream=True)
                                if 'content-length' in response.headers.keys():
                                    fileSize =int(response.headers['content-length'])
                                    # 更新数据库
                                    updateDatabase(name = videoTitle,date = datetime.now().strftime(('%Y-%m-%d %H:%M:%S')), preview_url = webmVideoUrl, detail_url = hyperlink, size = round(fileSize / size_limit, 2))
                                    print('[Info] Content-Length is: {0:.2f} MB'.format(fileSize / size_limit))
                                    if fileSize <= size_limit:
                                        print('[Downloading..] {0}'.format(videoFilePath))
                                        with open(videoFilePath, 'wb') as f:
                                            f.write(response.content)
                                        video_idx = video_idx + 1
                                    else:
                                        msg = '[Error] {0} size: {1:.2f} MB has exceed the limit: {2:.2f} MB.'.format(videoTitle, fileSize / size_limit, size_limit / size_limit)
                                        print(msg)
                                else:
                                    print('Content-Length not found.')
                            except Exception as e:
                                t,v,tb = sys.exc_info()
                                traceback.print_tb(tb)
                                print(e)
                                count += 1
                                continue
                            count += 1
                            print('progress of {0} {1}: {2} / {3}  {4}%'.format(category, folderName, count, totalCount, round(float(count)/totalCount * 100, 2)))
                            # 10 秒抓一个，防止被 ban。
                            time.sleep(10)
            except Exception as e:
                t,v,tb = sys.exc_info()
                traceback.print_tb(tb)
                continue

if __name__ == "__main__":
    fetchPreviewVideos()
    pass