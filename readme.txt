1.共有接口和作业所述相同
  debug_print: 用于测试打印的
2.私有方法包括了
	a.__next_token(self)
	  解析lua table string, 并转换成 python的dict或list
	  按作业要求检查了key是否是string或int，value是否为table, nil, int, string, boolean
	  其子方法包含了__parse_white(self)：解析空格，回车等；__parse_comments(self)： 解析注释；
			__parse_luatbl(self)： 解析table对象； __parse_bracket(self)：解析[]； __parse_string(self):解析字符串； __parse_num(self)：解析数值
	  
	b. __dump_parse(self)
       成员转lua table，解析dict
	   其子方法包含了__dump_parse_string(self, to_parse_str)：解析字符串；__dump_parse_dict(self, to_parse_dict)：解析字典；
	   ____dump_parse_list(self, to_parse_arr)：解析list；__dump_parse_other(self, value)：解析boolean，none，num等类型 
	   
    c. __save_file(self, f, s), __read_file(self, f)
		存取文件
	
	e. __deep_copy(self, input_dict)
		拷贝字典，取出不合法key
	  