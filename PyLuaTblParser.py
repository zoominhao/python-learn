#coding=utf-8
#!/usr/bin/python
__author__ = '竹明'
__date__ = '2015-02-06'


class PyLuaTblParser():
    "netease hw about Lua table Parser"

    # public
    def __init__(self):
        self.__luadict = {}  # dict or list, set dict as default
        self.__at = 0
        self.__len = 0
        self.__luastr = ''
        self.__container = []

    def load(self, s):
        "read Lua table, can handle with the wrong format"
        if not s or not isinstance(s, str):
            self.__parse_exception('Input is not string!')

        self.__luadict = {}   #clear member data
        self.__at = 0
        self.__len = len(s)
        self.__luastr = s
        self.__container = []

        self.__next_token()


    def dump(self):
        "return member in Lua table format"
        if not isinstance(self.__luadict, dict):
            self.__parse_exception('It is not dict!')

        return self.__dump_parse()

    def loadLuaTable(self, f):
        "read Lua table from file, f is file path, can handle with the wrong Lua table format and file exception"
        self.load(self.__read_file(f))

    def dumpLuaTable(self, f):
        "store member in Lua table format, f is file path, cover if file exists and throw the file handle exception"
        self.__save_file(f, self.dump())

    def loadDict(self, d):
        "read Dict data, only process the number key and string key"
        if not isinstance(d, dict):
            self.__parse_exception('It is not dict!')
        self.__luadict = self.__deep_copy(d)

    def dumpDict(self):
        "return a dict, do not directly return the member"
        if not self.__luadict:
            self.__parse_exception('Dict of Object is None')
        return self.__deep_copy(self.__luadict)

    def debug_print(self):
        print self.__luadict

    def update(self, d):
        "like the update method of class Dict"
        if len(self.__luadict) != 0:
            self.__luadict.update(d)
            return self.__luadict
        else:
            return {}

    def __getitem__(self, key):
        if len(self.__luadict) != 0:
            if key in self.__luadict.keys():
                return self.__luadict[key]
            else:
                print "Key doesn't exist"
                return None
        print "Empty Dict"
        return None

    def __setitem__(self, key, value):
        self.__luadict[key] = value

    def __next_token(self):
        value = None
        self.__parse_white()
        self.__parse_comments()
        ch = self.__luastr[self.__at]
        if ch == '{':
            self.__at += 1
            self.__parse_luatbl()
            return
        elif ch == '}' or ch == ',':
            self.__at += 1
            return ch
        elif ch == '"' or ch == "'":
            value = self.__parse_string()
            self.__tbl_insert(value)
            return value
        elif ch == '+' or ch == '-' or (ch >= '0'and ch <= '9'):
            value = self.__parse_num()
            self.__tbl_insert(value)
            return value
        elif ch == '[':
            self.__container[len(self.__container) - 1]['type'] = 'dict'
            self.__parse_bracket()
            return
        else:
            lastpos = self.__at

            while self.__at < self.__len and (self.__luastr[self.__at].isalnum() or self.__luastr[self.__at]=='_'):
                    self.__at += 1
            ch = self.__luastr[lastpos: self.__at]
            self.__parse_white()
            self.__parse_comments()
            if self.__luastr[self.__at] == '=':
                self.__at += 1
                self.__container[len(self.__container)-1]['type'] = 'dict'
                self.__container[len(self.__container)-1]['key'] = ch
                return
            else:
                if ch == 'true':
                    value = True
                elif ch == 'false':
                    value = False
                elif ch == 'nil':
                    value = None
                else:
                    self.__parse_exception('Error value')
                self.__tbl_insert(value)
                return value

    def __parse_white(self):
        "remove Backspace, Horizontal Table, Vertical Table, Carriage Return, Form Feed"
        while (self.__at < self.__len) and (self.__luastr[self.__at] in [' ', '\t', '\v', '\r', '\n', '\f']):
            self.__at += 1

    def __parse_comments(self):
        "remove comment line: single line comment -- and multiple line comment--[[...--]] and --[=[...--]=]"
        while self.__at < self.__len:
            if self.__at + 8 < self.__len and self.__luastr[self.__at: self.__at + 4] == '--[[':    #multiple line
                self.__at = self.__luastr.find('--]]', self.__at + 5)
                if self.__at < 0:
                    self.__parse_exception("Comment is not in right format!")
                else:
                    self.__at += 4
            elif self.__at + 10 < self.__len and self.__luastr[self.__at: self.__at + 5] == '--[=[':   #multiple line
                self.__at = self.__luastr.find('--]=]', self.__at + 6)
                if self.__at < 0:
                    self.__parse_exception("Comment is not in right format!")
                else:
                    self.__at += 5
            elif self.__at + 2 < self.__len and self.__luastr[self.__at: self.__at + 2] == '--':   #single line
                self.__at += 2
                while self.__at < self.__len and self.__luastr[self.__at] != "\n":
                    self.__at += 1
                self.__at += 1
            else:
                break
            while (self.__at < self.__len) and (self.__luastr[self.__at] in [' ', '\t', '\v', '\r', '\n', '\f']):
                self.__at += 1

    def __parse_luatbl(self):
        if len(self.__container) == 0:  #root
            self.__luadict = {}
            self.__container.append({'dict': self.__luadict, 'key': None, 'type': 'array', 'maxi': 1, 'p_key': 'root'})
        else:
            self.__container.append({'dict': {}, 'key': None, 'type': 'array', 'maxi': 1, 'p_key': None})
            self.__tbl_insert(self.__container[len(self.__container)-1])

        pos = self.__luastr.find('}', self.__at)
        if pos < 0:
            self.__parse_exception('Table struct is wrong!')

        # handle key or value
        jdgvalue = self.__next_token()
        while jdgvalue != '}':  #not empty table
            # handle value
            if self.__container[len(self.__container)-1]['key']:
                value = self.__next_token()
            # handle comma
            value = self.__next_token()
            if value == '}':
                break
            if value != ',':
                self.__parse_exception('Table struct is wrong!')


            #handle key or value
            value = self.__next_token()
            if value == '}':
                break

        # trans dict without string key into arr
        if len(self.__container) > 1:
            index = len(self.__container)-1
            last = index - 1
            if self.__container[index]['type'] =='array' and len(self.__container[index]['dict']) > 0:
                reversekey = self.__container[index]['p_key']
                self.__container[last]['dict'][reversekey] = self.__container[index]['dict'].values()
            del self.__container[index]

    def __parse_bracket(self):
        "parse [key]"
        self.__at += 1

        self.__parse_white()
        self.__parse_comments()

        ch = self.__luastr[self.__at]
        if ch == '"' or ch == '\'':
            self.__container[len(self.__container)-1]['key'] = self.__parse_string()   #key
        elif ch == '+' or ch == '-' or '0' <= ch <= '9':
            self.__container[len(self.__container)-1]['key'] = self.__parse_num()
        else:
            self.__parse_exception('Table struct is wrong!')

        self.__parse_white()
        self.__parse_comments()
        if self.__luastr[self.__at] != ']':
            self.__parse_exception('Table struct is wrong!')
        self.__at += 1

        self.__parse_white()
        self.__parse_comments()
        if self.__luastr[self.__at] != '=':
            self.__parse_exception('Table struct is wrong!')
        self.__at += 1

    def __parse_string(self):
        "parse string, care about escape"
        escape2char = {'a': '\a', 'r': '\r', 'b': '\b', 'f': '\f', 'n': '\n', 't': '\t', '\'': '\'', '"': '"', 'v': '\v',
                       '\\': '\\'}
        arr = []
        quote = self.__luastr[self.__at]
        self.__at += 1
        while True:
            escpos = self.__luastr.find('\\', self.__at)
            quotepos = self.__luastr.find(quote, self.__at)
            if escpos == -1 and quotepos == -1:
                self.__parse_exception('Unexpected end of string!')
            if escpos > 0 and (quotepos == -1 or quotepos > escpos):
                nextpos = escpos
            else:
                nextpos = quotepos
            if nextpos > self.__at:
                arr.append(self.__luastr[self.__at: nextpos])
                self.__at = nextpos
            if nextpos == quotepos:
                self.__at += 1
                break
            else:
                self.__at = nextpos + 1
                escchar = self.__luastr[self.__at]
                if escchar == 'u' or escchar == 'x':
                    self.__parse_exception('Include u or x!')
                elif escchar >= '0' and escchar <= '9':
                    endpos = self.__at + 1
                    if self.__luastr[self.__at + 1] >= '0' and self.__luastr[self.__at + 1] <= '9':
                        if self.__luastr[self.__at + 2]>='0' and self.__luastr[self.__at + 2] <= '9':
                            endpos = self.__at + 3
                        else:
                            endpos = self.__at + 2
                    value = chr(int(self.__luastr[self.__at: endpos]))
                    self.__at = endpos
                else:
                    value = escape2char[escchar]
                    self.__at += 1
                arr.append(value)
        return ''.join(arr)

    def __parse_num(self):
        "parse number, care about -,+ and e(E)"
        last, ch = self.__at, self.__luastr[self.__at]
        while '0' <= ch <= '9' or ch == 'e' or ch == 'E' or ch == '.' or ch == '+' or ch == '-':
            if self.__luastr[self.__at: self.__at + 2] == '--':
                break
            self.__at += 1
            if self.__at >= self.__len:
                break
            ch = self.__luastr[self.__at]
        try:
            value = eval(self.__luastr[last: self.__at])
        except Exception, e:
            self.__parse_exception("Num parse error!")
        return value

    def __tbl_insert(self, value):
        if isinstance(value, dict):
            last = len(self.__container) - 2
            if self.__container[last]['type'] == 'dict':
                key = self.__container[last]['key']
                if key:
                    self.__container[last]['dict'][key] = value['dict']
                    value['p_key'] = key
                    self.__container[last]['key'] = None
                else:
                    key = self.__container[last]['maxi']
                    self.__container[last]['dict'][key] = value['dict']
                    value['p_key'] = key
                    self.__container[last]['maxi'] += 1
            else:
                key = self.__container[last]['maxi']
                self.__container[last]['dict'][key] = value['dict']
                self.__container[last]['maxi'] += 1
        else:
            cur = len(self.__container) - 1
            key = self.__container[cur]['key']
            if self.__container[cur]['type'] == 'dict':
                if key:
                    if value != None:
                        self.__container[cur]['dict'][key] = value
                    self.__container[cur]['key'] = None
                else:
                    key = self.__container[cur]['maxi']
                    self.__container[cur]['dict'][key] = value
                    self.__container[cur]['maxi'] += 1
            elif self.__container[cur]['type'] == 'array':
                key = self.__container[cur]['maxi']
                self.__container[cur]['dict'][key] = value
                self.__container[cur]['maxi'] += 1

    def __dump_parse(self):
        self.__container = []
        self.__dump_parse_dict(self.__luadict)
        return ''.join(self.__container)

    def __dump_parse_dict(self, to_parse_dict):
        "parse dict"
        self.__container.append('{')
        self.__container.append('\n')
        if not isinstance(to_parse_dict, dict):
            self.__parse_exception('It is not dict')
        for key in to_parse_dict:
            #key
            value = to_parse_dict[key]
            self.__container.append('[')
            if isinstance(key, (int, float)):
                self.__container.append(str(key))
            elif isinstance(key, str) or isinstance(key, unicode):
                self.__container.append(self.__dump_parse_string(key))
            else:
                self.__parse_exception('Dict is not correct')
            self.__container.append(']')
            self.__container.append('=')

            #value
            if isinstance(value, dict):
                self.__dump_parse_dict(value)
            elif isinstance(value, list):
                self.__dump_parse_list(value)
            elif isinstance(value, str) or isinstance(value, unicode):
                self.__container.append(self.__dump_parse_string(value))
            else:
                self.__dump_parse_other(value)

            self.__container.append(',')
            self.__container.append('\n')
        self.__container.append('}')

    def __dump_parse_string(self, to_parse_str):
        char2escape = {"\a": "\\a", "\r": "\\r", "\b": "\\b", "\f": "\\f", "\n": "\\n",
                     "\t": "\\t", "'": "\\'", "\"": "\\\"", "\v": "\\v", "\\": "\\\\"}
        buf = []
        buf.append('"')
        if not isinstance(to_parse_str, (str, unicode)):
            self.__parse_exception('It is not list')
        for i in range(len(to_parse_str)):
            if to_parse_str[i] in char2escape:
                buf.append(char2escape[to_parse_str[i]])
            else:
                buf.append(to_parse_str[i])
        buf.append('"')
        return str(''.join(buf))

    def __dump_parse_list(self, to_parse_arr):
        "parse list"
        self.__container.append('{')
        if not isinstance(to_parse_arr, list):
            self.__parse_exception('It is not list')
        for i in range(len(to_parse_arr)):
            value = to_parse_arr[i]
            if isinstance(value, dict):
                self.__dump_parse_dict(value)
            elif isinstance(value, list):
                self.__dump_parse_list(value)
            elif isinstance(value, (str, unicode)):
                self.__container.append(self.__dump_parse_string(value))
            else:
                self.__dump_parse_other(value)

            self.__container.append(',')
        self.__container.append('}')

    def __dump_parse_other(self, value):
        "parse boolean, none, num"
        typeTransDict = {'None': 'nil', 'True': 'true', 'False': 'false'}
        if str(value) in typeTransDict:
            self.__container.append(typeTransDict[str(value)])
        elif isinstance(value, (int,float)):
            self.__container.append(str(value))
        else:
            self.__parse_exception('Data is not correct!')

    def __save_file(self, f, s):
        "save file"
        try:
            file_handler = open(f, "w")
        except IOError, open_err:
            print open_err
        else:
            try:
                file_handler.write(s)
            except IOError, write_err:
                print write_err
            else:
                print "SAVE SUCCESS"
            finally:
                file_handler.close()

    def __read_file(self, f):
        "read file"
        luatbl_str = ""
        try:
            file_handler = open(f, "r")
        except IOError, open_err:
            print open_err
        else:
            try:
                luatbl_str = file_handler.read()
            except IOError, read_err:
                print read_err
            else:
                print "READ SUCCESS"
            finally:
                file_handler.close()
        return luatbl_str

    def __deep_copy(self, input_dict):
        output_dict = {}
        if len(input_dict) == 1 and not isinstance(input_dict.items()[0][1], dict):
            if isinstance(input_dict.items()[0][0], (int, float, str, unicode)):
                return input_dict
            else:
                return output_dict


        for key, value in input_dict.items():
            v_output_dict = {}
            if isinstance(value, dict):
                for vkey, vvalue in value.items():
                    v_output_dict.update(self.__deep_copy({vkey: vvalue}))
            else:
                v_output_dict = value
            output_dict.update({key: v_output_dict})
        return output_dict

    def __parse_exception(self, errstr):
        raise Exception, errstr