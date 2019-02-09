# -*- coding: utf-8 -*-
"""
保存数据
Chinese Name
English Name
Employee ID
Resign 是否离职
Region 区域，包括省份和驻外国家
Gender
First Department
Second Department
Third Department
Fourth Department
Fifth Department
Sixth Department
Seventh Department
Office
Mobile
Email
"""

import pymongo
# import json

class OperDB(object):
    def __init__(self, dbName, tableName):
        self.open(dbName, tableName)

    def open(self, dbName, tableName):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        dblist = myclient.database_names()
        if dbName in dblist:
            print("dbName is exist: ", dbName)
        mydb = myclient[dbName]
        collist = mydb.collection_names()
        if tableName in collist:
            print("table is exist: ", tableName)
        self.client = myclient
        self.mydb = mydb
        mycol = mydb[tableName]
        self.mycol = mycol
    def addData(self, data):
        # data_str = json.dumps(data)
        try:
            self.mycol.insert_one(data)
        except Exception as e:
            print(e)



 

