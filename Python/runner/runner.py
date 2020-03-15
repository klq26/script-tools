import time
import sys
import re
import os
import threading
# from dingtalk import dingtalk


class myThread (threading.Thread):

    # interval 时间间隔, unit 单位（秒，分钟，小时，天）,targetClock（如果 unit 为 天，设置具体执行时间）, command 命令
    def __init__(self, interval, unit, targetClock, command):
        threading.Thread.__init__(self)
        self.interval = interval
        self.unit = unit
        self.targetClock = targetClock
        self.command = command

    def run(self):
        if self.unit not in ['second', 'min', 'hour', 'day']:
            print('时间单位 unit 不合法，不予执行')
            return
        self.runCommand(self.interval, self.unit,
                        self.targetClock, self.command)

    # 时间转秒。如：09:00:00 -> 123456
    def clockToSeconds(self, sTime):
        p="^([0-9]+):([0-5][0-9]):([0-5][0-9])$"
        cp=re.compile(p)
        try:
            mTime=cp.match(sTime)
        except TypeError:
            return "[InModuleError]:time2itv(sTime) invalid argument type"
    
        if mTime:
            t=list(map(int,mTime.group(1,2,3)))
            return 3600*t[0]+60*t[1]+t[2]
        else:
            return "[InModuleError]:time2itv(sTime) invalid argument value"

    def runCommand(self, intervalWithoutnit, unit, targetClock, command):

        if unit == 'second':
            interval = intervalWithoutnit
        elif unit == 'min':
            interval = intervalWithoutnit * 60
        elif unit == 'hour':
            interval = intervalWithoutnit * 3600
        elif unit == 'day':
            interval = intervalWithoutnit * 86400

        self.print_ts("-"*100)
        self.print_ts("Command {0}".format(command))
        self.print_ts("Starting every %s seconds." % interval)
        self.print_ts("-"*100)
        time_remaining = 0
        if interval < 86400:
            time_remaining = interval - time.time() % interval
        else:
            # 有特定时间点
            if len(targetClock) > 0:
                deltaSeconds = self.clockToSeconds(targetClock)
                time_remaining = interval - time.time() % interval - 8 * 3600 + deltaSeconds
            else:
                time_remaining = interval - time.time() % interval - 8 * 3600
        while True:
            try:
                # 如果算出来是负数，说明今天的该时间点已经过去，加一天到明天（86400秒）
                if time_remaining < 0:
                    time_remaining = time_remaining + 86400
                # 秒转人类可读模式
                m, s = divmod(int(round(time_remaining,0)), 60)
                h, m = divmod(m, 60)
                untilSecondsString = ("%d:%02d:%02d" % (h, m, s))
                
                self.print_ts("Sleeping until %s (waiting for %s)..." %
                    (time.strftime("%Y-%m-%d %H:%M:%S",(time.localtime(time.time()+time_remaining))), untilSecondsString))
                time.sleep(time_remaining)
                # 第一次设置完不完整间隔后，还要把 time_remaining 重置
                time_remaining = interval - time.time() % interval
                self.print_ts("Starting command: \"{0}\"".format(command))
                # execute the command
                status = os.system(command)
                self.print_ts("-"*100)
                self.print_ts("Command status = %s." % status)
            except Exception as e:
                print(e)
                # dingtalk().sendMessage('市值：{0}'.format(e))

    def print_ts(self, message):
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("{0} {1}".format(ts, message))

if __name__ == "__main__":
    # 金融接口

    # 检查今天的日期类型（工作日，周末，节假日）
    # datetimeCheckerThread = myThread(1,'day','2:00:00', 'python datetimeChecker.py')
    # # 获取 同花顺 - 涨跌分布（每分钟）
    # tonghuashunThead = myThread(1,'min','', 'python zdfbSpider.py')
    # # 获取 东方财富网 - 融资融券余额（每天）
    # eastMoneyThead = myThread(1,'day','9:15:00', 'python rzrqyeSpider.py')
    # # 执行任务
    # datetimeCheckerThread.start()
    # tonghuashunThead.start()
    # eastMoneyThead.start()

    # 视频业务（每 3 天执行一次）
    pornlibThread = myThread(3,'day','2:00:00','python ./pornlibSpider.py')
    pornlibThread.start()
