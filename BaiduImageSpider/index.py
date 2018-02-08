#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
import argparse
import sys
# 设置超时
import time

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.time_sleep = t

    # 保存图片
    def __save_image(self, rsp_data, word):
        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir('./' + word)) + 1
        for image_info in rsp_data['imgs']:
            try:
                time.sleep(self.time_sleep)
                fix = self.__get_suffix(image_info['objURL'])
                urllib.request.urlretrieve(image_info['objURL'], './' + word + '/' + str(self.__counter) + str(fix))
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                print(word+"+1,已有" + str(self.__counter) + "张"+word)
                self.__counter += 1
        return

    # 获取后缀名
    @staticmethod
    def __get_suffix(name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 获取前缀
    @staticmethod
    def __get_prefix(name):
        return name[:name.find('.')]

    # 开始获取
    def __get_images(self, word='美女'):
        # // tn:resultjsonavatarnew
        # // ie:utf - 8字符编码（ie输入 oe输出）
        # // word:美女 搜索关键字
        # // pn:60 开始条数
        # // rn:30 显示数量
        # // z:0 尺寸（0全部尺寸 9特大 3大 2中 1小）
        # // width:1024 自定义尺寸 - 宽
        # // height:768 自定义尺寸 - 高
        # // ic:0 颜色(0全部颜色 1红色 2黄色 4绿色 8青色 16蓝色 32紫色 64粉色
        # 128棕色 256橙色 512黑色 1024白色 2048黑白)
        # // s:0 3头像图片
        # // face:0 1面部特写
        # // st:-1 - 1全部类型 1卡通画 2简笔画
        # // lm:-1(6动态图片 7静态图片)
        # // gsm:3c pn值的十六进制数
        search = urllib.parse.quote(word)
        pn = self.__start_amount
        while pn < self.__amount:

            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            
            try:

                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                #print (req)
                page = urllib.request.urlopen(req)
               # print (page)
                rsp = page.read().decode('unicode_escape')
                #print (rsp)

               
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                # 解析json
                rsp_data = json.loads(rsp)
                self.__save_image(rsp_data, word)
                # 读取下一页
                print("下载下一页")
                pn += 60
            finally:
                page.close()
        print("下载任务结束")
        return

    def start(self, word, spider_page_num=1, start_page=1):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param spider_page_num: 需要抓取数据页数 总抓取图片数量为 页数x60
        :param start_page:起始页数
        :return:
        """
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.__get_images(word)

def main(argv):
    parser = argparse.ArgumentParser(description="Image Downloader")
    parser.add_argument("keywords", type=str,help='抓取的关键词. ("in quotes")')
    parser.add_argument("page_num", type=int,help='需要抓取数据页数 总抓取图片数量为 页数x60. ("in quotes")')
    parser.add_argument("start_page", type=int,help='起始页数')
    args = parser.parse_args(args=argv)
    crawler = Crawler(0.05)
    crawler.start(args.keywords, args.page_num, args.start_page)

if __name__ == '__main__':
    main(sys.argv[1:])
    
    





