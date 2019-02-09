# -*- coding: utf-8 -*-
"""
保存数据
1.Chinese Name
2.English Name
3.Employee ID
4.Resign 是否离职
5.Region 区域，包括省份和驻外国家
6.Gender
7. First Department
Second Department
Third Department
Fourth Department
Fifth Department
Sixth Department
Seventh Department
8.Office
9.Mobile
10.Email
11.备注
"""
import re
import constants

class Clean(object):
    @staticmethod
    def getChineseName(data):
        return data[0]

    @staticmethod
    def getEnglishName(data):
        return data[1]

    @staticmethod
    def getEmployeeId(data):
        #3.获取工号，字段3，通常是全数字/WX数字/空
        value = data[2]

        #匹配数字结尾的字串失败，返回空，否则返回默认值
        result = re.findall("\d+$", value)
        if not result:
            return ""
        return value

    @staticmethod
    def getGender(data):
        value = data[3]

        #如果性别不对，默认返回空串
        if value != "male" and value != "female":
            return ""
        return value
    
    @staticmethod
    def getDepartment(data):
        #中文名，英文名，工号，性别，部门，办公电话/地址，手机号，地址，邮箱
        if len(data) < 5:
            return ""
        #拆分返回列表
        x = data[4].split(">")
        return x
    
    @staticmethod
    def getOffice(data):
        #中文名，英文名，工号，性别，部门，办公电话/地址，手机号，地址，邮箱
        if len(data) < 6:
            return ""
        return data[5]
    
    @staticmethod
    def getEmail(data):
        #中文名，英文名，工号，性别，部门，办公电话/地址，手机号，地址，邮箱
        if len(data) < 9:
            return ""
        return data[8]
    
    @staticmethod
    def getMobile(data):
        #中文名，英文名，工号，性别，部门，办公电话/地址，手机号，地址，邮箱
        if len(data) < 7:
            return ""
        return data[6]

    @staticmethod
    def getResign(data):
        #中文名，英文名，工号，性别，部门，办公电话/地址，手机号，地址，邮箱
        email = Clean.getEmail(data)
        result = re.findall("notesmail", email)
        if result or len(data) < 6:
            resign = True
        else:
            resign = False
        return resign
    @staticmethod
    def getRegion(data):
        region = ""
        #1.地区部
        values = Clean.getDepartment(data)
        for value in values:
            pattern = re.compile('地区部')
            m = pattern.search(value)
            # m = re.match('地区部', value)
            if m:
                region = value[0:m.span()[0]]
                
        #2.代表处
        for value in values:
            pattern = re.compile('代表处')
            m = pattern.search(value) 
            if m:
                region += value[0:m.span()[0]]
        return region
        
    @staticmethod
    def wash(data):
        info = {}
        #1.获取中文名，字段1
        cName = Clean.getChineseName(data)
        info["Chinese Name"] = cName

        #2.获取英文名，字段2
        eName = Clean.getEnglishName(data)
        info["English Name"] = eName

        #3.获取工号，字段3，通常是全数字/WX数字/空
        eId = Clean.getEmployeeId(data)
        info["Employee ID"] = eId

        #4.是否在职，根据邮箱notesmail.huawei.com，或者根据字段，字段不完整的通常是离职状态，依赖邮箱
        resign = Clean.getResign(data)
        info["Resign"] = str(resign)

        #5.获取区域，根据部门名称判断区域，比如说XXX代表处前缀，也可根据手机号码前缀判断区域，依赖手机号码和部门
        region = Clean.getRegion(data)
        info["Region"] = region

        #6.性别，字段4
        gender = Clean.getGender(data)
        info["Gender"] = gender

        #7.获取多级部门，最多7级，将多级部门拆解，得到字段分布
        values = Clean.getDepartment(data)
        for i in range(len(values)):
            info[constants.departments[i]] = values[i]

        #8.获取办公电话
        office = Clean.getOffice(data)
        info["Office"] = office

        #9.获取手机号码
        mobile = Clean.getMobile(data)
        info["Mobile"] = mobile

        #10.获取邮箱
        email = Clean.getEmail(data)
        info["Email"] = email
        
        #11.备注
        info["Notes"] = " ".join(data)

        return info