#coding=utf-8
from selenium import webdriver
import time
import xlwt
from xlwt import Workbook,easyxf,Formula

browser = webdriver.Firefox()
browser.maximize_window()
browser.get("http://www.jd.com/pinpai/751-8544.html")
time.sleep(5)
links = browser.find_elements_by_css_selector("li.gl-item div.p-name a")

items=[]
for link in links:
    print(link.text)
    print(link.get_attribute("href"))
    item={}
    item['name']=link.text
    item['url']=link.get_attribute("href")
    item['type']='电风扇'
    items.append(item)

workbook= xlwt.Workbook()

table = workbook.add_sheet('wahson',cell_overwrite_ok=True)
table.col(0).width = 15000
table.col(1).width = 10000
table.col(2).width = 7000


style = xlwt.XFStyle()    # 初始化样式
font = xlwt.Font()        # 为样式创建字体
font.bold = True
style.font = font         #为样式设置字体

table.write(0,0,'型号',style)    
table.write(0,1,'型号产品链接',style) 
table.write(0,2,'类别',style)  

link_style = easyxf('font: underline single')
i=1
for item in items:
    table.write(i,0, item['name'])    
    table.write(i,1,Formula('HYPERLINK("'+item['url']+'";"'+item['url']+'")'),link_style)    
    table.write(i,2,item['type'])
    i=i+1
    
workbook.save("d:/wahson2.xls") 

time.sleep(5)
browser.close()
