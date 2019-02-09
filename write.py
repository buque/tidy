 # -*- coding: utf-8 -*-
"""
清洗数据
"""
import xlrd
import threading
import queue
import time
from clean import Clean
from db import OperDB

class Writer(threading.Thread):
    writeSum = 0
    writeLock = None
    queue = None
    dbName = ""

    def __init__(self, threadName, dbName, queue):
        threading.Thread.__init__(self)
        self.threadName = threadName
        if Writer.dbName is None:
            Writer.dbName = dbName
        if Writer.queue is None:
            Writer.queue = queue
        if Writer.writeLock is None:
            Writer.writeLock = threading.Lock()
        self.db = OperDB(dbName, "test6")
    
    def putData(self, data):
        self.db.addData(data)

    def run(self):
        #本地变量，减少锁并发冲突
        times = 0
        etimes = 0
        print ("Starting ", self.threadName, "...")

        while True:
            try:
                value = Writer.queue.get_nowait()
            except queue.Empty:
                etimes += 1
                if etimes%50 == 0 and times != 0:
                    Writer.writeLock.acquire()
                    Writer.writeSum += times
                    Writer.writeLock.release()
                    times = 0
                    etimes = 0
                    time.sleep(0.5)
                    continue
            else:
                data = Clean.wash(value)
                self.putData(data)
                times += 1

                #多线程数据加锁
                if times%50 == 0:
                    Writer.writeLock.acquire()
                    Writer.writeSum += times
                    Writer.writeLock.release()
                    times = 0
    

