# -*- coding:utf-8 -*-
from Tkinter import *
from ScrolledText import ScrolledText
import urllib
import requests
import re
import threading
import time


def get(ID):
    varl.set('已经获取到第%s本书' % ID)
    html = urllib.urlopen('https://read.douban.com/ebooks/tag/%E5%B0%8F%E8%AF%B4/?cat=book&sort=top&start=' + str(ID)).read()
#    print html
    reg = r'<span class="price-tag ">(.*?)元</span>.*?read.douban.com\'\)">(.*?)</a>'
    print reg
#    reg = r'<span class="price-tag ">(.*?)元</span>< a href=".*?" .*?read.douban.com\'\)">(.*?)</a>'
#    reg = r'< span class ="price-tag " > (.* ?)元 < / span > < a href=".*?" target="_blank" class ="btn btn-icon " > 试读 < / a > < / div > < a data-target-dialog="login" href="#" class ="require-login btn btn-info btn-cart " > < i class ="icon-cart" > < / i > < span class ="btn-text" > 加入购物车 < / span > < / a > < / div > < div class ="title" > < a href=".*?" onclick="moreurl\(this, {&#39;aid&#39;: &#39;.*?&#39;, &#39;src&#39;: &#39;tag&#39;}, true, \'read.douban.com\'\)" > (.* ?) </a> '
    reg = re.compile(reg)#编译提高效率
    return re.findall(reg,html)#匹配，类型list

#a = get()

#计算书本数量的函数
def wirte():

    ID = 0#申明变量
    a = []
    s = 0
    while ID <= 5:
        L = get(ID)#获取书名和价格
        ID += 20
        for i in L:
            s+=1
            a.append(float(i[0]))
            text.insert(END,'书名：%s      价格：%s\n' % (i[1],i[0]))
    text.insert(END,'------------------------------------------\n')
    text.insert(END,'该分类书本总数量%s\n' %s)
    text.insert(END,'书本的总价格%s\n' %sum(a))
    text.insert(END,'平均每本%.2f' %(sum(a)/s))
    fn= open('read.txt','W')
    fn.wirte(text.get(1.0,END)).encode('gdk')
    fn.close()
    varl.set('全部处理完成')

def th():
    t1 =  threading.Thread(target=wirte)
    t1.start()

# 创建一个窗口
root = Tk()
root.geometry('800x500+200+200')#窗口大小,是小写字母x,且没有空格

# 窗口的标题
root.title('python college')
# 文本滚动窗口
text = ScrolledText(root,font=('Courier New',10))
text.grid()

button = Button(root,text = '开始爬虫',font =('微软雅黑',10),command=th)#添加按钮
button.grid()

# 设置Lable
varl = StringVar()#通过一个tk方法绑定一个变量
label = Label(root,font=('微软雅黑',10),fg='red',textvariable=varl)
label.grid()

varl.set('Ready!')

root.mainloop()#进去消息循环，发送命令
