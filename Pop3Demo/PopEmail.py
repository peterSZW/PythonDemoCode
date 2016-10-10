#-*- encoding: gb2312 -*-
import os, sys, string
import poplib
import sqlite3

from email.parser import Parser


host = "pop.ym.163.com"
username = "xx@xx.com"
password = "x"

pp = poplib.POP3(host) #pp.set_debuglevel(1)
pp.user(username)
pp.pass_(password)
ret = pp.stat()
print 'login:',ret



# connection database

con =sqlite3.connect("PopEmail.db")
try:
    #con.execute("create table catalog (id integer primary key,pid integer,name varchar(10) UNIQUE,nickname text NULL)")
    con.execute("create table emails (id integer primary key AUTOINCREMENT, messageID varchar(50) UNIQUE,subject varchar(200),body text NULL)")
    con.commit()
except:
    print 'Table already Exists'


# looping data

for i in range(1, ret[0]+1):
    mlist = pp.top(i, 0)
    print 'line: ', len(mlist[1])
    #print mlist
    headerStr = ''
    for line in mlist[1]:
        headerStr = headerStr+line+'\n'

    #print headerStr
    headers = Parser().parsestr(headerStr)
    messageID = headers['Message-ID']
    print messageID
    t = (headers['Message-ID'],)

    cx=con.execute("select count(*) from emails where messageID = ?",t)
    data = cx.fetchall()
    if data[0][0]==0:
        print 'NO DATA'
    else:
        print 'YES'





    # ȡ���ż�ͷ����ע�⣺topָ�������������ż�ͷΪ�����ģ�Ҳ����˵��ȡ0�У�
    # ��ʵ�Ƿ���ͷ����Ϣ��ȡ1����ʵ�Ƿ���ͷ����Ϣ֮���ٶ�1�С�

# �г����������ʼ���Ϣ��������ÿһ���ʼ������id�ʹ�С������stat��������ܵ�ͳ����Ϣ
ret = pp.list()
print 'list:', ret
# ȡ��һ���ʼ�������Ϣ���ڷ���ֵ��ǰ��д洢��down[1]���б���ġ�down[0]�Ƿ��ص�״̬��Ϣ
down = pp.retr(1)
print 'lines:', len(down)
s = ''
for line in down[1]:
    s = s+line+'\n'
headers = Parser().parsestr(s)


#con = sqlite3.connect(":memory:")





if 0:
    #  Now the header items can be accessed as a dictionary:
    print 'To: %s' % headers['to']
    print 'From: %s' % headers['from']
    print 'Subject: %s' % headers['subject']
    print 'Message-ID: %s' % headers['Message-ID']

    t = (headers['Message-ID'],headers['subject'],s)
    con.execute("insert into emails(messageID,subject,body) values (?,?,?)", t)
    con.commit()




pp.quit()