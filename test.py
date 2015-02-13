#coding=utf-8
#!/usr/bin/python
__author__ = '竹明'

from PyLuaTblParser import PyLuaTblParser



a1 = PyLuaTblParser()
#case in requirement
# print "case1\n"
#
# test_str = '{array = {65,23,5},dict = {mixed = {43,54.33,false,nil,{string = "value"}},array = {3,6,4,},{string = "value"},},}'
# #test_str = '{65,23}'
# a1.load(test_str)
# a1.debug_print()
# d1 = a1.dump()
# print d1
#
a2 = PyLuaTblParser()
a2.loadLuaTable("case1_in.txt")
a2.debug_print()
a2.dumpLuaTable("case1_out.txt")
#
#
# a3 = PyLuaTblParser()
# a3.loadLuaTable("case1_out.txt")
# d3 = a3.dumpDict()
# print d3
# a3.loadDict(a1.dumpDict())
# a3.debug_print()

#case with Exception
# print "case2\n"
# exp_str1 = '{array = {65,23,5,,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
# exp_str2 = '{array = {65,23,fg5,},dict = { = "value",},array = {3,6,4,},string = "value",},}'
# exp_str3 = '{array = {65,23,5,},dict = {mixed = {43,54...33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
# exp_str4 = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",}'
# exp_str5 = '{array = [65,23,5,,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
# exp_str6 = '{array = [65,23,5,,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = value",},}'
# a4 = PyLuaTblParser()
# a4.load(exp_str1)
# a4.load(exp_str2)
# a4.load(exp_str3)
# a4.load(exp_str4)
# a4.load(exp_str5)
# a4.load(exp_str6)
#
# exp_str7 = '{{{1,4,6},4},5,"43"}'
# a4.load(exp_str7)
# a4.debug_print()

# print "case3\n"
# a5 = PyLuaTblParser()
# dict_1 = {
#      "array": [65, 23, 5],
#      "dict": {
#           "mixed": {
#                1: 43,
#                2: 54.33,
#                3: False,
#                4: 9,
#                "string": "value"
#           },
#           "array": [3, 6, 4],
#           "string": "value"
#      }
# }
#
# dict_2 = {
#      "array": [65, 23, 5],
#      "dict": {
#           "mixed": {
#                1: 43,
#                2: 54.33,
#                3: False,
#                4: 9,
#                a1: "value"
#           },
#           "array": [3, 6, 4],
#           "string": "value"
#      }
# }
#
# dict_3 = {}
#
# a5.loadDict(dict_1)
# a5.debug_print()
#
# a5.loadDict(dict_2)
# a5.debug_print()
#
# a5.loadDict(dict_1)
# a5.debug_print()
# dict = a5.dumpDict()
# print(dict)

#advanced
# print "case4\n"
# a6 = PyLuaTblParser()
# a6.loadLuaTable("case1_in.txt")
# tmpDict = {
#      "array": [65, 23, 5],
#      "dict": {
#           "mixed": {
#                1: 43,
#                2: 54.33,
#                3: False,
#                4: 9,
#                "string": "value"
#           },
#           "array": [3, 9, 4],
#           "string": "132",
#           "tw": "va"
#      }
# }
# a6.debug_print()
# dict = a6.update(tmpDict)
# print(dict)
#
# a6.debug_print()
#
# a6["array1"] = [34, 16]
# a6.debug_print()