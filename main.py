 # -*- coding: utf-8 -*-
"""
主进程
"""
import queue
import time
from read import Reader
from write import Writer

fileName = ".\\store1.xls"

class Tidy(object):
    queue = None
    writeList = []

    @staticmethod
    def createQueue():
        Tidy.queue = queue.Queue()

    @staticmethod
    def createReader():
        reader = Reader("reader", fileName, Tidy.queue)
        reader.start()

    @staticmethod
    def createWriters(dbName, threadNum):
        for i in range(0, threadNum):
            writer = Writer("writer"+str(i), dbName, Tidy.queue)
            writer.start()
            Tidy.writeList.append(writer)

if __name__=="__main__":
    #创建多线程的共享通信队列
    Tidy.createQueue()
    
    #启动单线程读取excel
    Tidy.createReader() 

    #启动多线程实例并发清洗数据并存入
    Tidy.createWriters("test", 2)

    #循环等待
    while True:
        time.sleep(1)
        
        #打印多线程信息
        print("Read sum is: ", Reader.readSum)
        print("Write sum is: ", Writer.writeSum)