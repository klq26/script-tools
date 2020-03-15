# -*- coding: utf-8 -*-
import os
from os import path
import sys

import pymysql

# 把选择的视频名称组成数组
def getSelectedVideosName(folderpath):
    results = []
    for root, dirs, files in os.walk(folderpath):
        for file in files:
            if '.mp4' in file:
                results.append(file.replace('.mp4',''))
    return results

# 从数据库获取详情页地址数组
def getDetailUrlFromDB(detailurls):
    print('Total Number: %s' % len(detailurls))
    temp = ["\'{0}\'".format(x) for x in detailurls]
    values = ",".join(temp)
    # 动态选择数据库服务器地址（如果在 server 端运行，没必要走外网地址）
    ip_address = ''
    if sys.platform.startswith('win'):
        ip_address = '112.125.25.230'
    elif sys.platform.startswith('linux'):
        ip_address = '127.0.0.1'
    db = pymysql.connect(ip_address,'klq26','abc123!@#==','video_unique')
    cursor = db.cursor()
    sql = r"SELECT detail_url from pornlib WHERE name IN ({0})".format(values)
    # print(sql)
    cursor.execute(sql)
    cursor.close()
    db.close()
    detailurl_list = [x[0] for x in list(cursor.fetchall())]
    for x in detailurl_list:
        if sys.platform.startswith('win'):
            os.startfile(x)
        elif sys.platform.startswith('linux'):
            print(x)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        results = getSelectedVideosName(sys.argv[1]) # r'C:\Users\kangliquan\Desktop\20200315'
        getDetailUrlFromDB(results)
    else:
        print('[Error] missing video folder path.')
