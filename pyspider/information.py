# coding:utf-8
import requests
from bs4 import BeautifulSoup
import operator as op
import re
import urllib
import xlwt
#药材-资讯信息
def saveInfor():
    user_agent = 'Mozilla/4.0 (compatible;MSIE5.5;windows NT)'
    headers = {'User-Agent': user_agent}
    Host = 'https://www.zyctd.com/zixun-'
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('information')
    head = ['key','title','intro','author','time','url']  # 表头
    num=1
    for h in range(len(head)):
        sheet.write(0, h, head[h])  # 写入表头
    for x in range(3,1000):
        data=[]
        res = requests.get(Host + str(x) +'.html', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser', from_encoding='utf-8')
        zixun_items=soup.find_all(class_="zixun-item")
        for item in zixun_items:
            title = item.find_all("span")[0].text
            intro = item.find_all(class_="content-text")[0].text.strip()
            time = item.find_all(class_="item-footer")[0].find_all("span")[0].text.strip()
            author = item.find_all(class_="item-footer")[0].find_all("span")[1].text.strip()[4:].lstrip()
            try:
                key = item.find_all(class_="product-name")[0].text.strip()
            except:
                key="无"
            url = 'https://www.zyctd.com/'+item.find_all("a")[0].get('href')
            if key!="无":
                data.append({
                    'key':key,
                    'title':title,
                    'author':author,
                    'intro':intro,
                    'time':time,
                    'url':url
                })
        for one in data:
            sheet.write(num, 0, one['key'])
            sheet.write(num, 1, one['title'])
            sheet.write(num, 2, one['intro'])
            sheet.write(num, 3, one['author'])
            sheet.write(num, 4, one['time'])
            sheet.write(num, 5, one['url'])
            num=num+1
        if num%50==0:
            print(num)
    book.save('information.xls')
    # book.save('E:/WU/pyfile/xin/pos.xls')
if __name__=="__main__":
    saveInfor()














