# coding=utf-8

'''
陈坤峰
'''

'''打开指定的json文件，并将其转化为str类型'''


def jsonToStr(f = "json.txt"):
    with open(f,"r",encoding="utf-8") as file:
        content = file.readlines()      # 读取文件中的所有内容，并将其按行存为列表
    str=""
    for eachLine in content:           # 转换为字符串
        for i in range(len(eachLine)):
            str+=eachLine[i]
    return str



'''封装解析器类'''


class JsonParser(object):

    def __init__(self,str=None):      # 初始化时，传入一个属性变量str，即json字符串
        self.str = str
        self.index = 0         # 遍历字符串的索引变量

    def skipBlank(self):      # 忽略json的空白
        while (self.index<len(self.str)) and (self.str[self.index] in ' \n\t\r'):
            self.index=self.index+1

    '''以上为文件的预处理，以下为具体的解析过程'''

    def parse(self):

        self.skipBlank()
        if self.str[self.index]=='{':       #如果识别出“{”则可判定下文中为object类型
            self.index += 1
            return  self.parse_object()
        elif self.str[self.index] == '[':   #如果识别出“{”则可判定下文中为array类型
            self.index+=1
            return self.parse_array()
        else:
            print('未成功解析json')

    '''锁定双引号，以此确定json中的string类型'''
    def parse_string(self):
        start = end = self.index        # 找到string的范围
        while self.str[end] != '"':
            if self.str[end] == '\\':  # \，表明其后面的是配合\的转义符号，如\",\t,\r，主要针对\"的情况
                end += 1
                if self.str[end] not in '\\/bfnrtu':
                    continue
            end += 1
        self.index = end+1
        return self.str[start:end]

    '''解析number类型'''
    def parse_number(self):
        start = end = self.index
        end__str = '  \n\t\r,}]'                # 数字结束的字符串
        while self.str[end] not in end__str:  # 如果没遇到数字结束的标志，就继续向后
            end += 1
        number = self.str[start:end]

        # 对于用科学计数法表示的浮点数进行转换
        if '.' in number or 'e' in number or 'E' in number:
            number = float(number)
        else:
            number = int(number)
        self.index = end
        return number

    '''解析json的value部分'''
    def parse_value(self):
        c = self.str[self.index]

        #解析object
        if c == '{':
            self.index+=1
            self.skipBlank()
            return self.parse_object()

        # 解析array
        elif c == '[':
            self.index += 1
            self.skipBlank()
            return self.parse_array()
        # 解析string
        elif c == '"':
            self.index += 1
            self.skipBlank()
            return self.parse_string()
        # 解析bool变量
        elif c == 't' and self.str[self.index:self.index+4] == 'true':
            self.index += 4
            return True
        elif c=='f' and self.str[self.index:self.index+5] == 'false':
            self.index += 5
            return False
        #  其余的即为number
        else:
            return self.parse_number()

    '''解析array'''
    def parse_array(self):
        arr = []
        self.skipBlank()
        if self.str[self.index]==']':       # 判断是否为空数组
            self.index += 1
            return arr
        while True:
            value = self.parse_value()
            arr.append(value)    # 获取array中的值，并将其添加至列表变量
            self.skipBlank()
            if self.str[self.index] == ',':
                self.index += 1
                self.skipBlank()
            elif self.str[self.index] == ']':
                self.index += 1
                return arr
            else:
                print("无法解析array")
                return None


    '''解析object'''
    def parse_object(self):
        obj = {}
        self.skipBlank()
        if self.str[self.index]=='}':   # 判断object是否为空
            self.index += 1
            return obj

        self.index += 1      # 跳过object外面的花括号
        while True:
            key = self.parse_string()   #获取对象的key
            self.skipBlank()

            self.index = self.index+1   # 跳过键值之间的冒号
            self.skipBlank()
            obj[key] = self.parse_value()
            self.skipBlank()

            if self.str[self.index] == '}':
                self.index += 1
                break       #对象结束
            elif self.str[self.index]==',':     # 若存在其他对象
                self.index += 1
                self.skipBlank()
            self.index += 1
        return obj

    def display(self):
        displayStr = ""
        self.skipBlank()
        while self.index < len(self.str):
            displayStr = displayStr+self.str[self.index]
            self.index += 1
            self.skipBlank()
        print(displayStr)


'''把python对象重新编码为json字符串'''


def pythonToJson(py):
    str_ = ''
    if(type(py) == type({})):   # 处理对象
        str_ +='{'
        notNull = False
        for key in py:
            if type(key) == type(''):
                notNull = True  #对象非空
                str_ += '"'+key+'":'+pythonToJson(py[key])+','
        if notNull:
            str_ = str_[:-1]  # 把最后的逗号去掉
        str_ +='}'

    elif type(py) == type([]):  #处理数组
        str_ += '['
        if len(py)>0:
            str_ += pythonToJson(py[0])
        for i in range(1,len(py)):
            str_ += ','+pythonToJson(py[i])
        str_ +=']'

    elif type(py) == type(''):  # 处理字符串
        str_ = '"'+py+'"'
    elif py == True:
        str_ += 'true'
    elif py == False:
        str_ += 'false'
    elif py == None:
        str_ +='null'
    else:
        str_ = str(py)
    return str_


'''主函数'''
if __name__ == '__main__':
    jsonstr = jsonToStr('Test1.txt')
    print("以下为解析结果:\n")
    jsonparser = JsonParser(jsonstr)
    jsonTmp = jsonparser.parse()
    # 以下为利用json库实现的解析,用之对照验证
    import json
    print("原json串:\n",jsonstr)
    print("json库实现解析:\n",str(json.loads(jsonstr)))
    print("jsonpaser实现解析:\n",jsonTmp)
    print("重新将python编码成json:\n",pythonToJson(jsonTmp))