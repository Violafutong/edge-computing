#coding:utf-8
import socket
import sys
import MySQLdb
import itselfip
import makefile
import conn
'''
正式版
'''
#:输入ip
ip=sys.argv[1]
flag=True
try:
    sql='update task set gets=1,ip="'+ip+'",status=0 where gets=0 limit 1'
    conn.mysql_execute(sql,'commit')
    sql='select id,runs from task where gets=1 and ends=0 and ip="'+ip+'"'
    result = conn.mysql_execute(sql,'fetchone')
    if result == None:
        sql='update task set gets=1,ip="'+ip+'",status=0 where gets=1 and ends=0 and status=1 limit 1'
        conn.mysql_execute(sql,'commit')
        sql='select id,runs from task where gets=1 and ends=0 and ip="'+ip+'" limit 1'
        result = conn.mysql_execute(sql,'fetchall')
        if result == ():
            flag=False
            #:没有查询到任务，返回done
            print('done')
        else:
            #:将数据库中已经被提取但是设备出错的任务返回
            id=result[0][0]
            run=result[0][1]
            #here print the command and id
            print(run+'$'+str(id))
    else:
        #:将未被提取的任务返回
        id=result[0]
        run=result[1]
        print(run+'&'+str(id))

except MySQLdb.Error as e:
    print("Mysql Error%d:%s"% (e.args[0],e.args[1]))

