 # -*- coding: utf-8 -*-
"""
读取数据
"""
import xlrd
import threading
import queue


class Reader(threading.Thread):
    readSum = 0
    queue = None

    def __init__(self, threadName, fileName, queue):
        threading.Thread.__init__(self)  
        self.threadName = threadName
        self.fileName = fileName
        Reader.queue = queue
    
    def openFile(self, sheetIndex):
        try:
            self.workbook = xlrd.open_workbook(self.fileName, "utf8")
        except Exception as e:
            print(e)
            return False
        else:
            self.sheet = self.workbook.sheets()[sheetIndex]
            return True

    def run(self):
        print ("Starting", self.threadName, "...")
        self.openFile(0)
        nrows = self.sheet.nrows

        for i in range(0, nrows):
            row_value = self.sheet.row_values(i)
            Reader.queue.put(row_value)
            Reader.readSum += 1
        

