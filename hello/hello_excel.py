#coding=utf-8
import xlwt

workbook= xlwt.Workbook()
# 注意这里的Workbook首字母是大写
#tablesheetrkbook.add_sheet('sheet name')  # 新建一个sheet
# 写入数据table.write(行,列,value)
# 如果对一个单元格重复操作，会引发
# returns error:
# Exception: Attempt to overwrite cell:
# sheetname=u'sheet 1' rowx=0 colx=0
# 所以在打开时加cell_overwrite_ok=True解决

table = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
table.write(0,0,'cctest')
# 另外，使用style
style = xlwt.XFStyle()    # 初始化样式
font = xlwt.Font()        # 为样式创建字体
font.name = 'Times New Roman'
font.bold = True
style.font = font         #为样式设置字体
table.write(0, 0, 'some bold Times')
# 使用样式
workbook.save('d:/demo.xls')     # 保存文件
