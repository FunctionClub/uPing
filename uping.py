#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
import commands
import sys

class Pinger():
    STYLE = {
        'fore': {
            'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
            'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
        },
        'back': {
            'black': 40, 'red': 41, 'green': 42, 'yellow': 43,
            'blue': 44, 'purple': 45, 'cyan': 46, 'white': 47,
        },
        'mode': {
            'bold': 1, 'underline': 4, 'blink': 5, 'invert': 7,
        },
        'default': {
            'end': 0,
        }
    }

    def __init__(self, host):
        self.start_time = time.localtime(time.time())
        self.start_time_m = time.time()

        self.data = dict()
        self.host = host

        self.midnight_zero = list()
        self.midnight_non_zero = list()
        self.morning_zero = list()
        self.morning_non_zero = list()
        self.afternoon_zero = list()
        self.afternoon_non_zero = list()
        self.night_zero = list()
        self.night_non_zero = list()






    def ping(self):
        cmd = "ping "+ self.host + " -c1 -W 1"
        result = commands.getoutput(cmd)
        result = result.split()
        result = result[-2].split("/")[0]
        if result.isalpha():
            result =0
        return float(result)


    def use_style(self,string, mode='', fore='', back=''):
        mode = '%s' % self.STYLE['mode'][mode] if self.STYLE['mode'].has_key(mode) else ''
        fore = '%s' % self.STYLE['fore'][fore] if self.STYLE['fore'].has_key(fore) else ''
        back = '%s' % self.STYLE['back'][back] if self.STYLE['back'].has_key(back) else ''
        style = ';'.join([s for s in [mode, fore, back] if s])
        style = '\033[%sm' % style if style else ''
        end = '\033[%sm' % self.STYLE['default']['end'] if style else ''
        return '%s%s%s' % (style, string, end)

    def red(self,str):
        return self.use_style(str,fore="red")

    def blue(self,str):
        return self.use_style(str,fore="blue")

    def cyan(self,str):
        return self.use_style(str,fore="cyan")

    def yellow(self,str):
        return self.use_style(str,fore="yellow")

    def green(self,str):
        return self.use_style(str,fore="green")

    def purple(self,str):
        return self.use_style(str,fore="purple")

    def colored(self,latency):
        if latency == 0:
            return self.red(str(round(latency,2)) + " ms")
        elif(0<latency < 100):
            return self.green(str(round(latency,2)) + " ms")
        elif latency < 170:
            return self.yellow(str(round(latency,2)) + " ms")
        else:
            return self.red(str(round(latency,2)) + " ms")


    def start(self):
        current_time = time.localtime(time.time())
        i=1

        while(time.time() - self.start_time_m <= 86400):

            latency=self.ping()
            current_time = time.localtime(time.time())
            self.data[i] = {"year":  current_time[0], \
                            "month": current_time[1], \
                            "day" :  current_time[2], \
                            "hour" : current_time[3], \
                            "minute":current_time[4], \
                            "second":current_time[5],\
                            "latency": latency}

            i = i + 1
            self.print_graph()
            self.data.clear()

            if(latency != 0.0):
                time.sleep(1)





    def is_night(self,d):
        if  18 <= d["hour"] <= 23:
            return True
        else:
            return False

    def is_morning(self,d):
        if 6 <= d["hour"] <= 12:
            return True
        else:
            return False

    def is_mid_night(self,d):
        if 0 < d["hour"] < 6:
            return True
        else:
            return False

    def is_afternoon(self,d):
        if 12 < d["hour"] < 18:
            return True
        else:
            return False

    def lost_percentage(self,zero,non_zero):

        sum = len(zero) + len(non_zero)

        if sum == 0:
            return self.red(str(0) + " %")
        else:
            percentage = 100 * len(zero) / sum

        if percentage <5:
            return self.green(str(int(percentage)) + " %")
        elif percentage < 10:
            return self.yellow(str(int(percentage)) + " %")
        else:
            return self.red(str(int(percentage)) + " %")

    def print_graph(self):
        os.system("clear")
        spend_time = (time.time() - self.start_time_m)

        for i in self.data.keys():

            x = self.data[i]
            latency = x["latency"]

            total_count = self.data.keys()[-1]

            if(self.is_mid_night(x)):
                if latency == 0:
                    self.midnight_zero.append(latency)
                else:
                    self.midnight_non_zero.append(latency)

            elif(self.is_morning(x)):
                if latency == 0:
                    self.morning_zero.append(latency)
                else:
                    self.morning_non_zero.append(latency)

            elif(self.is_afternoon(x)):
                if latency == 0:
                    self.afternoon_zero.append(latency)
                else:
                    self.afternoon_non_zero.append(latency)

            elif(self.is_night(x)):
                if latency == 0:
                    self.night_zero.append(latency)
                else:
                    self.night_non_zero.append(latency)
            else:
                print("Error :", x)




        total_non_zero = self.morning_non_zero + self.midnight_non_zero + self.afternoon_non_zero+self.night_non_zero

        total_zero_list = self.morning_zero + self.midnight_zero + self.afternoon_zero+self.night_zero
        total_zero = len(total_zero_list)

        if(total_count - total_zero == 0):
            total_average = 0
        else:
            total_average = sum(total_non_zero)/(total_count - total_zero)

        if len(self.morning_non_zero) == 0:
            morning_average = 0
        else:
            morning_average = sum(self.morning_non_zero) / len(self.morning_non_zero)

        if len(self.afternoon_non_zero) == 0:
            afternoon_average = 0
        else:
            afternoon_average = sum(self.afternoon_non_zero) / len(self.afternoon_non_zero)

        if len(self.night_non_zero) == 0:
            night_average = 0
        else:
            night_average = sum(self.night_non_zero) / len(self.night_non_zero)

        if len(self.midnight_non_zero) == 0:
            midnight_average = 0
        else:
            midnight_average = sum(self.midnight_non_zero) / len(self.midnight_non_zero)

        print("-" * 53)
        print("|{0:16}{1:37}{2:16}|".format("",self.cyan("服务器延迟监测脚本"),""))
        print("-" * 53)
        print "| {0:37}| {1:37}|".format(self.blue("上午统计"),self.blue("下午统计"))
        print("{0:39}| {1:37}|".format("| 最低延迟: " + self.colored(  min(self.morning_non_zero) if len(self.morning_non_zero)!=0 else 0),"最低延迟: " + self.colored(min(self.afternoon_non_zero) if len(self.afternoon_non_zero) != 0 else 0)  )  )
        print("{0:39}| {1:37}|".format("| 最高延迟: " + self.colored(max(self.morning_non_zero) if len(self.morning_non_zero)!=0 else 0),"最高延迟: " + self.colored(max(self.afternoon_non_zero) if len(self.afternoon_non_zero) != 0 else 0)))
        print("{0:39}| {1:37}|".format("| 平均延迟: " + self.colored(morning_average),"平均延迟: " + self.colored(afternoon_average)))
        print("{0:38}| {1:36}|".format("| 丢包率  : "+ self.lost_percentage(self.morning_zero,self.morning_non_zero),"丢包率  : " + self.lost_percentage(self.afternoon_zero,self.afternoon_non_zero)))
        print("{0:39}| {1:37}|".format("| 超时次数: " + self.red(len(self.morning_zero)),"超时次数: " + self.red(len(self.afternoon_zero))))
        print("{0:30}| {1:28}|".format("| 测试次数: " + str(len(self.morning_non_zero) + len(self.morning_zero)),"测试次数: " + str(len(self.afternoon_non_zero) + len(self.afternoon_zero))))



        print("-" * 53)
        print "| {0:37}| {1:37}|".format(self.blue("夜晚统计"), self.blue("半夜统计"))
        print("{0:39}| {1:37}|".format(
            "| 最低延迟: " + self.colored(min(self.night_non_zero) if len(self.night_non_zero) != 0 else 0),
            "最低延迟: " + self.colored(min(self.midnight_non_zero) if len(self.midnight_non_zero) != 0 else 0)))
        print("{0:39}| {1:37}|".format(
            "| 最高延迟: " + self.colored(max(self.night_non_zero) if len(self.night_non_zero) != 0 else 0),
            "最高延迟: " + self.colored(max(self.midnight_non_zero) if len(self.midnight_non_zero) != 0 else 0)))
        print("{0:39}| {1:37}|".format("| 平均延迟: " + self.colored(night_average),
                                       "平均延迟: " + self.colored(midnight_average)))
        print("{0:38}| {1:36}|".format("| 丢包率  : "+ self.lost_percentage(self.night_zero,self.night_non_zero),"丢包率  : " + self.lost_percentage(self.midnight_zero,self.midnight_non_zero)))
        print("{0:39}| {1:37}|".format("| 超时次数: " + self.red(len(self.night_zero)),
                                       "超时次数: " + self.red(len(self.midnight_zero))))
        print("{0:30}| {1:28}|".format("| 测试次数: " + str(len(self.night_non_zero) + len(self.night_zero)),
                                       "测试次数: " + str(len(self.midnight_non_zero) + len(self.midnight_zero))))


        print("-" * 53)
        print "| {0:63}|".format(self.blue("全局统计"))
        print("{0:41}{1:36}|".format("| 最低延迟: " + self.colored(min(total_non_zero) if len(total_non_zero) != 0 else 0),"丢包率    : " + self.lost_percentage(total_zero_list,total_non_zero)))
        print("{0:41}{1:38}|".format("| 最高延迟: " + self.colored(max(total_non_zero) if len(total_non_zero) != 0 else 0),"总超时次数: " + self.red(total_zero)))
        print("{0:41}{1:29}|".format("| 平均延迟: " + self.colored(total_average),"总测试次数: " + str(total_count)))


        print("-" * 53)
        print ("|{0:13}{1:30}{2:22}{3:9}|".format("", self.purple("当前测试Ping值:"), self.colored(self.data[self.data.keys()[-1]]["latency"]),""))
        print("-" * 53)

        print("|{0:12}{1:4}{2:2} 小时{3:2} 分钟{4:2} 秒{5:13}|".format("",self.purple("已耗时:"),int(spend_time/3600)if spend_time/3600 >=1 else 0,(int(spend_time % 3600 /60))if spend_time % 3600 /60 >= 1 else 0,int(spend_time % 3600 %60),""))
        print("-" * 53)



if __name__ == "__main__" :
    os.system("clear")
    print("服务器延迟监测脚本")
    print("Made By 主机博客（zhujiboke.com）")
    print("")
    mytime = time.localtime(time.time())
    print("当前服务器时间为: " + str(mytime[0]) + "年" + str(mytime[1]) + "月" + str(mytime[2]) +"日 "  + str(mytime[3]) + ":" + str(mytime[4]) + ":" + str(mytime[5]) )
    myinput = raw_input("是否正确 (y/n): ")

    if myinput == "y":
        pinghost = raw_input("请输入要Ping的服务器IP/域名：")
        p = Pinger(pinghost)
        p.start()
    else:
        print("\n请将服务器时间调整正确后运行本程序！")
