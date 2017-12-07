#!/usr/bin/env python
#encoding: utf-8
#description:
#笔趣看读书网站小说抓取器 http://www.biqukan.com/
#功能：
#   1、整理抓取文字格式
#   2、排除重复章节

import urllib
import bs4
import re


#  小说信息配置
story_name = "我是大玩家"
target_url = "http://www.biqukan.com/26_26459/"

#读取小说内容
def readContent(download_url):

    # test download_url = "http://www.biqukan.com/1_1094/5403177.html"
    head = {}
    head['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    download_req = urllib.request.Request(url = download_url, headers = head)
    download_response = urllib.request.urlopen(download_req)
    download_html = download_response.read().decode("gbk","utf8")

    soup_texts = bs4.BeautifulSoup(download_html,'lxml')

    #内容
    texts = soup_texts.find_all(id = 'content', class_ = 'showtxt')
    soup_text = bs4.BeautifulSoup(str(texts), 'lxml')
    content = soup_text.div.text
    content = content.replace('\xa0' , '')
    content = content.replace('http://www.biqukan.com/1_1094/5403177.html　　请记住本书首发域名：www.biqukan.com。笔趣阁手机版阅读网址：m.biqukan.com' , '')

    return content

#读取小说文章列表
print("开始下载小说 《%s》 ...." % story_name)

head = {}
head['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
target_req = urllib.request.Request(url = target_url, headers = head)
target_response = urllib.request.urlopen(target_req)
target_html = target_response.read().decode('gbk','utf8')

listman_soup = bs4.BeautifulSoup(target_html, 'lxml')
chapters = listman_soup.find_all('div',class_ = 'listmain')
download_soup = bs4.BeautifulSoup(str(chapters), 'lxml')

begin_flag = False
num_cout = 1
index = 1
story = ""
pre_download_names = {}

#计算总章节
for child in download_soup.dl.children:
    if child == '\n':
        continue

    #不知道为什么正则表达式不包含《》匹配不到内容
    if re.match(r"《\w*》正文卷", child.string):
        begin_flag = True

    if begin_flag == True and child.a !=  None:
        download_name = child.string
        download_url = "http://www.biqukan.com/" + child.a['href']
        if re.match(r'\d+、\w+' , download_name):
            #排除掉重复章节
            #有连续重复，有隔章重复
            if download_name not in pre_download_names:
                # print(download_name + '=>' + str(num_cout))
                num_cout += 1
                pre_download_names[download_name] = download_url

for key in pre_download_names:
    print(key + " => " + pre_download_names[key])


#下载每章内容
for key in pre_download_names:
    download_content = ""
    download_content = readContent(pre_download_names[key])
    story = story + key + "\n"
    story = story + download_content + "\n"
    print("已下载：( %d / %d ) " % (index, num_cout) + "\r")
    index += 1

print("%s下载完毕，开始保存文件...." % story_name)
file = open(story_name + '.txt', 'w', encoding='utf-8')
file.write(story)
file.close()
print("文件保存完毕 => %s.txt." % story_name)
