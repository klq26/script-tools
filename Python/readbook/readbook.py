# -*- coding: utf-8 -*-
import os
import time
import platform

from alertThread import alertThread

# 操作系统 Linux or Win
platform_name = platform.system()

if __name__ == "__main__":
    # 每 30 秒提醒一次
    alert_interval = 30
    # 已计时次数
    alert_count = 0
    # 计时三十分钟
    alert_times = alert_interval * 60
    # 开始时间戳
    start_ts = int(time.time())
    # 咪咕阅读完毕次数
    # migu_finish_count = 34

    counting_down = alert_interval
    while(alert_count < alert_times / alert_interval):
        while(counting_down > 0):
            # 不换行打印倒计时
            print('\r{0}'.format(str(counting_down).zfill(2)), end='')
            counting_down -= 1
            time.sleep(1)
        alert_count += 1
        # play
        text = ''
        if platform_name.lower() == 'linux':
            text = f'Page {alert_count}'
        else:
            text = f'翻页第 {alert_count} 次'
        print(text)
        # 多线程播放声音，不卡计时主进程
        my_thread = alertThread(text = text)
        my_thread.start()
        counting_down = alert_interval
        # if alert_count == migu_finish_count:
            # text = u'咪咕读书打卡已完毕'
            # print(text)
            # my_thread = alertThread(text = text)
            # my_thread.start()
    
    if platform_name.lower() == 'linux':
        text = 'mission complete'
    else:
        text = '今日全部打卡已完毕'
    print(text)
    my_thread = alertThread(1, text = text)
    my_thread.start()
    pass
