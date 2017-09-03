# -*- coding:utf-8 -*-
from Tkinter import *
from ScrolledText import ScrolledText
import urllib
import requests
import re
import threading
import time


url_name=[]#url+name

a=1#页数
def get():
    global a#a改变全局变量，
    hd={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Lin… Gecko/20100101 Firefox/54.z'}
    url='http://www.budejie.com/video/'+str(a)
    varl.set('已经获取第%s页的视频'%(a))
    html=requests.get(url,headers=hd).text#发送请求
 #   print html
    url_content = re.compile(r'(<div class="j-r-list-c">.*?</div>.*?</div>)',re.S)
    url_contents = re.findall(url_content,html)
    for i in url_contents:
        url_reg = r'data-mp4="(.*?)">'
        url_items = re.findall(url_reg,i)
        print url_items
        if url_items:#如果有视频存在，就匹配名字，如果是图片，就跳过
            name_reg = re.compile(r'<a href="detail-.{8}.html">(.*?)</a>', re.S)
            name_items = re.findall(name_reg,i)
           # print name_items
            for i,k in zip(name_items,url_items):
                url_name.append([i,k])
 #               print i,k
    return url_name

id =1 #视频个数
def write():
    global id
    while id<10:
        url_name = get()#调用获取视频+名字
        for i in url_name:
            urllib.urlretrieve(i[1],'video/%s.mp4'%(i[0].decode('utf-8').encode('gbk')))#下载
            text.insert(END,str(id)+'.'+i[1]+'\n'+i[0]+'\n')
            url_name.pop(0)#删除第一个元素
            id+=1
    varl.set('视频抓取完毕，over')

def start():
    th = threading.Thread(target=write)
    th.start()


root = Tk()
root.title('bangbangda')
text = ScrolledText(root,font=('Courier New',10))
text.grid()
button = Button(root,text = 'start to crawl',font =('微软雅黑',10),command=start)
button.grid()
varl = StringVar()#通过一个tk方法绑定一个变量
label = Label(root,font=('微软雅黑',10),fg='red',textvariable=varl)
label.grid()
varl.set('Ready!')
root.mainloop()

