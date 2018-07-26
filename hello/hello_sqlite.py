#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入SQLite驱动:
import sqlite3
# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect('hello.db')
# 创建一个Cursor:
cursor = conn.cursor()
cursor.execute('drop table user')
# 执行一条SQL语句，创建user表:
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# 继续执行一条SQL语句，插入一条记录:
cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
cursor.execute('insert into user (id, name) values (\'2\', \'Jackson\')')
# 通过rowcount获得插入的行数:
print(cursor.rowcount)
# 查询:
print(cursor.execute('select * from user').fetchall())
print(cursor.execute('select * from user').fetchmany(size=1))
print(cursor.execute('select * from user').fetchone())


# 关闭Cursor:
cursor.close()
# 提交事务:
conn.commit()
# 关闭Connection:
conn.close()