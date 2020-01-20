#! /usr/bin/env python3
# -*- coding:utf-8 -*-

# Author   : puntsok
# Blog     : https://github.com/puntsokCN
# Date     : 2019/12/30
# Name     : analysis
# Software : vscode
# Note     : Word类           ：分析藏文字符组成元素 及判断其合法性。
# Note     : Auxiliary_Word类 ：分析藏文句子中格助词使用是否正确

class Word:

    """
    单词分析类
    1. 实例对象可调用相应的方式获取 对应的单词具体的组成元素
    2. 输入参数 对词终结符不做限制
    """

    def __init__(self, s):
         # 元素映射:[ 前    上    基    下    音标   后    重后]
        self.__result = [None, None, None, None, None,
                         None, None]  # 需要每次新建对象是初始化成 none元素 避免多对象间互相干扰
        if len(s) == 0:
            print("输入字符不可为空！")
        if s[-1] == "་" or s[-1] == "།":
            if len(s) <= 8:
                self.__str = s[:-1]
            else:
                print("输入字符过长")
        else:
            if len(s) <= 7:
                self.__str = s
            else:
                print("输入字符过长")

    #############################################################################
    # 私有数据
    __words = ['ཀ', 'ཁ', 'ག', 'ང', 'ཅ', 'ཆ', 'ཇ', 'ཉ', 'ཏ', 'ཐ', 'ད', 'ན',
               'པ', 'ཕ', 'བ', 'མ', 'ཙ', 'ཚ', 'ཛ', 'ཝ', 'ཞ', 'ཟ', 'འ', 'ཡ',
               'ར', 'ལ', 'ཤ', 'ས', 'ཧ', 'ཨ']
    __front = ["ག", "ད", "བ", "མ", "འ"]
    __top = ["ར", "ལ", "ས", "ག", "ད", "ཛ", "བ", "ཧ"]
    __below = ["ྱ", "ྲ", "ླ", "ྭ"]
    __behind = ["ག", "ང", "ད", "ན", "བ", "མ", "འ", "ར", "ལ", "ས"]
    __repeat_behind = ["ད", "ས"]   # ད 虽然也是重后加字，但是现代藏文里已弃用
    __symbol = ['ི',  'ུ',  'ེ', 'ོ',  'ཽ',  'ྀ',  'ཻ']
    __sub_word_dict = {'ཀ': 'ྐ',  'ཁ': 'ྑ',  'ག': 'ྒ',  'ང': 'ྔ',  'ཅ': 'ྕ',  'ཆ': 'ྖ',  'ཇ': 'ྗ',  'ཉ': 'ྙ',
                       'ཏ': 'ྟ',  'ཐ': 'ྠ',  'ད': 'ྡ',  'ན': 'ྣ',  'པ': 'ྤ',  'ཕ': 'ྥ',  'བ': 'ྦ',  'མ': 'ྨ',
                       'ཙ': 'ྩ',  'ཚ': 'ྪ',  'ཛ': 'ྫ',  'ཝ': 'ྭ',  'ཞ': 'ྮ',  'ཟ': 'ྯ',  'འ': 'ྰ',  'ཡ': 'ྱ',
                       'ར': 'ྲ', 'ལ': 'ླ',  'ཤ': 'ྴ',  'ས': 'ྶ',  'ཧ': 'ྷ',  'ཨ': 'ྸ'}
    __new_dict = dict(zip(__sub_word_dict.values(), __sub_word_dict.keys()))
    __sub_word = ['ྐ',   'ྑ',   'ྒ',   'ྔ',   'ྕ',   'ྖ',   'ྗ',   'ྙ',  'ྟ',   'ྠ',   'ྡ',   'ྣ',   'ྤ',   'ྥ',
                  'ྦ',   'ྨ',   'ྩ',   'ྪ',   'ྫ',   'ྮ',   'ྯ',   'ྰ',   'ྴ',   'ྶ',   'ྷ',   'ྸ']

    __special_words = ['ཛྙ', 'ཧྥ', 'གྷ',  'དྷ',  'ཛྷ', 'བྷ']

    # 上加字 正字规范
    __top_ra = ['ཀ', 'ག', 'ང', 'ཇ', 'ཉ', 'ཏ', 'ད', 'ན', 'བ', 'མ', 'ཙ', 'ཛ']
    __top_la = ['ཀ', 'ག', 'ང', 'ཇ', 'ཅ', 'ཏ', 'ད', 'པ', 'བ', 'ཧ']
    __top_sa = ['ཀ', 'ག', 'ང', 'ཉ', 'ཏ', 'ད', 'ན', 'པ', 'བ', 'མ', 'ཙ']

    # 下加字 正字规范
    __under_ya = ['ཀ', 'ཁ', 'ག', 'པ', 'ཕ', 'པ', 'མ']
    __under_ra = ['ཀ', 'ཁ', 'ག', 'ཏ', 'ད', 'པ', 'ཕ', 'བ', 'མ', 'ཤ', 'ས', 'ཧ']
    __under_la = ['ཀ', 'ག', 'བ', 'ཟ', 'ར', 'ས']
    __under_wa = ['ཀ', 'ཁ', 'ག', 'ཉ', 'ད', 'ཙ',
                  'ཚ', 'ཞ', 'ཟ', 'ར', 'ལ', 'ཤ', 'ས', 'ཧ']

    #############################################################################
    # 内调功能函数：修改 __result 元素  此区域函数能识别现代藏文词的构成元素。无法识别复杂的生僻词、大部分缩写词汇
    # 查找字符串的所有元素信息，并填充信息至 __result的行为函数，供外调函数 使用
    
    # 分析函数群的调度中心，只要满足其中之一的特征，即能定位出所有元素信息，剩余的函数就不必执行 -- 供外调函数调用
    def __analysis(self):
        "按序分析字符串，并保存信息至 __result"
        all = [self.__if_single, self.__if_top, self.__if_below,
               self.__if_symbol, self.__if_pure_word]
        for func in all:            # 只要字符满足其中之一特征，便可寻到所有元素
            if func():
                break

    #############
    # 根据词组成的具体特征，寻找所有元素的策略的函数群组
    
    # 根据 查找到的基字及其索引值 查找剩余所有元素、供 __if_* 函数调用
    def __find(self, index):
        """
        根据基字索引 寻找其他元素
        :param index: 基字 的索引值 
        """
        # 当字符只有一个字
        if len(self.__str) == 1:
            self.__result[2] = self.__str[index]
        # 若 基字前只有一个字
        if index == 1:
            if self.__str[index] in self.__sub_word:               # 如果基字 为下加形态，判断前项字符为 上加字
                self.__result[1] = self.__str[index-1]
            else:                                                   # 如果基字 为正常形态，判断前项字符为 前加字
                self.__result[0] = self.__str[index-1]

        # 若 基字前有两个字 则必为 前加字 + 上加字
        if index == 2:
            self.__result[1] = self.__str[index-1]
            self.__result[0] = self.__str[index-2]
        # 若基字后 有一个字符
        if len(self.__str)-index == 2:
            # 可能是 下加字--不在正字规范里判断，需记录错误字符、后续的同理
            if self.__str[index+1] in (self.__sub_word + self.__below):
                self.__result[3] = self.__str[index+1]
            if self.__str[index+1] in self.__symbol:               # 可能是 音标
                self.__result[4] = self.__str[index+1]
            if self.__str[index+1] in self.__words:                # 可能是 后加字
                self.__result[5] = self.__str[index+1]
            if self.__str[index+1] == "ཌ":                         # 可能是 缩写字
                self.__result[5] = "ག"
                self.__result[6] = "ས"
        # 若基字后 有两个字符
        if len(self.__str)-index == 3:
            if self.__str[index+1] in (self.__sub_word + self.__below):  # 如果 第一个是 下加字
                self.__result[3] = self.__str[index+1]              #
                if self.__str[index+2] in self.__symbol:           # 下加字 + 音标 的可能性
                    self.__result[4] = self.__str[index+2]          #
                if self.__str[index+2] in self.__words:            # 下加字 + 后加字的可能性
                    self.__result[5] = self.__str[index+2]          #
                if self.__str[index+2] == "ཌ":                     # 可能是 缩写字
                    self.__result[5] = "ག"
                    self.__result[6] = "ས"
            if self.__str[index+1] in self.__symbol:               # 如果 第一个是 音标
                if self.__str[index+2] == "ཌ":                     # 可能是 缩写字
                    self.__result[5] = "ག"
                    self.__result[6] = "ས"
                else:                                               # 音标 + 后加字
                    self.__result[4] = self.__str[index+1]          # 保存 音标
                    self.__result[5] = self.__str[index+2]          # 保存 后加字
            if self.__str[index+1] in self.__words:                # 如果 第一个是 后加字 第二个是重后加字
                self.__result[5] = self.__str[index+1]              # 保存 后加字
                self.__result[6] = self.__str[index+2]              # 保存 重后加字
        # 若基字后 有三个字符
        if len(self.__str)-index == 4:
            if self.__str[index+1] in (self.__sub_word + self.__below):  # 第一个是下加字的情景
                self.__result[3] = self.__str[index+1]
                if self.__str[index+2] in self.__symbol:
                    if self.__str[index+3] == "ཌ":                 # 可能是 缩写字
                        self.__result[4] = self.__str[index+2]      # 保存 音标
                        self.__result[5] = "ག"
                        self.__result[6] = "ས"
                    else:                                           # 下加字 + 音标 + 后加字
                        self.__result[4] = self.__str[index+2]      # 保存 音标
                        self.__result[5] = self.__str[index+3]      # 保存 后加字
                if self.__str[index+2] in self.__words:             # 下加字 + 后加字 + 重后加字
                    self.__result[5] = self.__str[index+2]          # 保存 后加字
                    self.__result[6] = self.__str[index+3]          # 保存 重后加字
            if self.__str[index+1] in self.__symbol:                # 音标 + 后加字 + 重后加字的情景
                self.__result[4] = self.__str[index+1]              # 保存 音标
                self.__result[5] = self.__str[index+2]              # 保存 后加字
                self.__result[6] = self.__str[index+3]              # 保存 重后加字
        # 若基字后 有四个字符
        if len(self.__str)-index == 5:                             # 必然是 下加字 + 音标 + 后加字 + 重后加字
            self.__result[3] = self.__str[index+1]
            self.__result[4] = self.__str[index+2]
            self.__result[5] = self.__str[index+3]
            self.__result[6] = self.__str[index+4]
    
    # 单字成词的情况 --- 查找基字及其索引值的策略
    def __if_single(self):
        """
        单字成词 མིང་གཞི་རྐྱང་པ་
        :return true: 如果程序执行返回 true   
        """
        if len(self.__str) == 1:
            self.__result[2] = self.__str[0]
            index = 0
            return True
        else:
            return False
    # 当存在上加字的情况 --- 查找基字及其索引值的策略
    def __if_top(self):
        """
        མགོ་ཅན་ཡོད་པ་  当存在上加字  寻找基字及其索引值
        :return true: 如果程序执行返回 true
        """

        if set(self.__str) & set(self.__sub_word):
            # 找到 下加形态的基字
            sub_word = [i for i in self.__str if i in self.__sub_word]
            # 考虑到特殊字的基字不是 下加形态 eg: གྷ
            index_sub = self.__str.index(
                sub_word[0])                    # 下加形态字符的 索引值
            if sub_word[0] in ["ྙ", "ྥ", "ྷ"]:
                if self.__str[index_sub-1] in ["ག", "ད", "ཛ", "བ", "ཧ"]:  # 如果是特殊字符 就做以下特殊处理
                    if (sub_word[0] == "ྙ") & ((self.__str[index_sub-1]) == "ཛ"):
                        index = index_sub
                        self.__result[2] = self.__str[index-1] + \
                            self.__str[index]             # 保存 基字
                        # 寻找其他元素
                        self.__find(index)
                        # 上加字为 None
                        self.__result[1] = None
                        # 下加字为 None
                        self.__result[3] = None
                    elif (sub_word[0] == "ྥ") & ((self.__str[index_sub-1]) == "ཧ"):
                        index = index_sub                                #
                        # 寻找其他元素
                        self.__find(index)
                        self.__result[2] = self.__str[index-1] + \
                            self.__str[index]             # 保存 基字
                        # 上加字为 None
                        self.__result[1] = None
                        # 下加字为 None
                        self.__result[3] = None
                    elif (sub_word[0] == "ྷ") & ((self.__str[index_sub-1]) in ["ག", "ད", "ཛ", "བ", "ཧ"]):

                        index = index_sub
                        self.__result[2] = self.__str[index-1] + \
                            self.__str[index]             # 保存 基字
                        # 寻找其他元素
                        self.__find(index)
                        # 上加字为 None
                        self.__result[1] = None
                        # 下加字为 None
                        self.__result[3] = None
                else:  # 虽然下加字是 特殊字的下加字  但是也存在 རྙ 等情况
                    index = index_sub
                    # 保存 基字
                    self.__result[2] = self.__new_dict[self.__str[index]]
                    self.__find(index)                               # 寻找其他元素
            else:  # 普遍情况
                index = index_sub                                           # 找到 基字 在字符串中的索引值
                # 保存 基字
                self.__result[2] = self.__new_dict[self.__str[index]]
                # 寻找其他元素
                self.__find(index)

            return True
        else:
            return False
    # 当存在下加字的情况 --- 查找基字及其索引值的策略
    def __if_below(self):
        """
        འདོགས་ཅན་ཡོད་པ་  当存在下加字  寻找基字及其索引值
        :return true: 如果程序执行返回 true
        """
        if set(self.__str) & set(self.__below):
            below_word = [
                i for i in self.__str if i in self.__below]   # 找到 下加字
            # 找到 基字 在字符串中的索引值
            index = self.__str.index(below_word[0]) - 1
            if self.__str[index] in self.__sub_word:                   # 根据基字形态 保存 基字
                self.__result[2] = self.__new_dict[self.__str[index]]
            else:
                self.__result[2] = self.__str[index]
            self.__find(index)                               # 寻找其他元素

            return True
        else:
            return False
    # 当存在音标的情况 --- 查找基字及其索引值的策略
    def __if_symbol(self):
        "དབྱངས་ཡོད་པ་  当存在音标 寻找基字及其索引值"
        if set(self.__str) & set(self.__symbol):
            # 找到 音标
            symbol = [i for i in self.__str if i in self.__symbol]
            symbol_index = self.__str.index(
                symbol[0])                      # 找到 音标的索引值
            if self.__str[symbol_index-1] in self.__below:                 # 当音标前是 下加字时
                index = symbol_index-2                                     # 找到 基字 的索引值
                if self.__str[index] in self.__sub_word:                   # 根据基字形态 保存 基字
                    self.__result[2] = self.__new_dict[self.__str[index]]
                else:
                    self.__result[2] = self.__str[index]
                self.__find(index)
            else:
                index = symbol_index - 1                                     # 找到 基字 的索引值
                if self.__str[index] in self.__sub_word:                   # 根据基字形态 保存 基字
                    self.__result[2] = self.__new_dict[self.__str[index]]
                else:
                    self.__result[2] = self.__str[index]
                self.__find(index)                               # 寻找其他元素
            return True
        else:
            return False
    # 当同时不存在上加字、下加字和音标时的情况下 --- 查找基字及其索引值的策略 
    def __if_pure_word(self):
        "当字符串里没有上加字、下加字、和音标时 寻找基字及 其他元素"
        # 保持 字符串里各元素存在的 信息 True为存在 Flase为不存在
        state = []
        state.append(bool(set(self.__str) & set(self.__symbol))
                     )            # 查看是否存在 音标
        state.append(bool(set(self.__str) & set(self.__sub_word))
                     )          # 查看是否存在 上加字
        state.append(bool(set(self.__str) & set(self.__below))
                     )             # 查看是否存在 下加字
        if True not in state:
            # 前加字 + 基字 + 后加字 + 重后加字的情景
            if len(self.__str) == 4:
                self.__result[0] = self.__str[0]
                self.__result[2] = self.__str[1]
                self.__result[5] = self.__str[2]
                self.__result[6] = self.__str[3]
            if len(self.__str) == 3:
                if self.__str[-1] == "ཌ":                                  # 可能是 缩写字
                    self.__result[0] = self.__str[0]
                    self.__result[2] = self.__str[1]
                    self.__result[5] = "ག"
                    self.__result[6] = "ས"
                # 如果最后一个字不是 重后加字， 则：前加字 + 基字 + 后加字
                if self.__str[-1] not in self.__repeat_behind and self.__str[-1] != "ཌ":
                    self.__result[0] = self.__str[0]
                    self.__result[2] = self.__str[1]
                    self.__result[5] = self.__str[2]
                if self.__str[-1] in self.__repeat_behind:
                    if self.__str[-1] == "ས":
                        # 当只有三个字根时：ས 的前项是这些字时，ས 作为 重后加字 存在
                        if self.__str[1] in ["ག", "ད", "བ", "མ"]:
                            self.__result[2] = self.__str[0]
                            self.__result[5] = self.__str[1]
                            self.__result[6] = self.__str[2]
                        else:
                            self.__result[0] = self.__str[0]
                            self.__result[2] = self.__str[1]
                            self.__result[5] = self.__str[2]

                    else:                                          # 重后加字 ད 已被弃用，一般三个字尾出现时，当做后加字
                        self.__result[0] = self.__str[0]
                        self.__result[2] = self.__str[1]
                        self.__result[5] = self.__str[2]
            if len(self.__str) == 2:                               # 当只有两个字  一般都是  基字 + 后加字 这样处理
                if self.__str[-1] == "ཌ":
                    self.__result[2] = self.__str[0]
                    self.__result[5] = "ག"
                    self.__result[6] = "ས"
                else:
                    if self.__str[0] in self.__front:
                        # 当第一个字符在 前加字集 且 第二个在后加字集时 eg བས་
                        if self.__str[1] in self.__behind:
                            self.__result[2] = self.__str[0]
                            self.__result[5] = self.__str[1]
                        else:                                       # 当第一个字符在 前加字集 且 第二个 不 在后加字集时 eg བཀ་
                            self.__result[0] = self.__str[0]
                            self.__result[2] = self.__str[1]
                    else:                                          # 当第一个字符不在 前加字集时  eg  ཀས

                        self.__result[2] = self.__str[0]
                        self.__result[5] = self.__str[1]
            return True
        else:
            return False
    
    ###### 
    # 审查 __result 各元素的合法性函数群组，供外调函数使用

    def __check_front(self):
        """
        审查 前加字
        :return str/None:  返回错误信息, 字符合法返回None
        """
        if self.__result[0] is not None:
            if self.__result[0] not in self.__front:
                return "不存在前加字(སྔོན་འཇུག་) {}".format(self.__result[0])

    def __check_top(self):
        """
        审查 上加字
        :return str/None:  返回错误信息, 字符合法返回None
        """
        if self.__result[1] is not None:

            if self.__result[1] in self.__top:

                # 若不是特殊字、则分别查看正字规范表
                if self.__result[1] + self.__result[2] not in self.__special_words:

                    if self.__result[1] == "ར":
                        if self.__result[2] not in self.__top_ra:
                            # 需要把基字转换成 下加形态打印
                            return ("上加字ra(མགོ་ཅན་ ར)的正字规范里不存在字符： {0} ！！".format(self.__result[1]+self.__sub_word_dict[self.__result[2]]))
                    if self.__result[1] == "ལ":
                        if self.__result[2] not in self.__top_la:
                            # 需要把基字转换成 下加形态打印
                            return "上加字la(མགོ་ཅན་ ལ)的正字规范里不存在字符： {0} ！！".format(self.__result[1]+self.__sub_word_dict[self.__result[2]])
                    if self.__result[1] == "ས":
                        if self.__result[2] not in self.__top_sa:
                            # 需要把基字转换成 下加形态打印
                            return ("上加字sa的正字规(མགོ་ཅན་ ས)范里不存在字符： {0} ！！".format(self.__result[1]+self.__sub_word_dict[self.__result[2]]))
                    else:      # 既不是特殊字 便是 也不是ra la sa 则为非法字
                        return ("不存在上加字(མགོ་ཅན་)： {}".format(self.__result[1]))

            else:
                return ("不存在上加字(མགོ་ཅན་)： {}".format(self.__result[1]))

    def __ckeck_under(self):
        """
        审查 下加字
        :return str/None:  返回错误信息, 字符合法返回None
        """
        if self.__result[3] is not None:
            # 当不在 正字规范里时
            if self.__result[3] not in self.__below:
                # 若不是特殊字、则分别查看正字规范表
                if (self.__result[2] + self.__result[3]) not in self.__special_words:
                    # 由于是非法的下加字 需要转换一下形态
                    return ("不存在下加字(འདོགས་ཅན་)： {}".format(self.__new_dict[self.__result[3]]))
            else:
                if self.__result[3] == "ྱ":
                    if self.__result[2] not in self.__under_ya:
                        return ("下加字 (འདོགས་ཅན་ ཡ་རྟགས་) ྱ 的规范里不存在字符: {}".format(self.__result[2]+self.__result[3]))
                if self.__result[3] == "ྲ":
                    if self.__result[2] not in self.__under_ra:
                        return ("下加字 (འདོགས་ཅན་ ར་རྟགས་) ྱ 的规范里不存在字符: {}".format(self.__result[2]+self.__result[3]))
                if self.__result[3] == "ླ":
                    if self.__result[2] not in self.__under_la:
                        return ("下加字 (འདོགས་ཅན་ ལ་རྟགས་) ྱ 的规范里不存在字符: {}".format(self.__result[2]+self.__result[3]))
                if self.__result[3] == "ྭ":
                    if self.__result[2] not in self.__under_wa:
                        return ("下加字 (འདོགས་ཅན་ ཝ་རྟགས་) ྱ 的规范里不存在字符: {}".format(self.__result[2]+self.__result[3]))

    def __check_behind(self):
        """
        审查 后加字
        :return str/None:  返回错误信息, 字符合法返回None
        """
        if self.__result[5] is not None:
            if self.__result[5] not in self.__behind:
                return ("不存在后加字(རྗེས་འཇུག་): {}".format(self.__result[5]))

    def __check_repeat_behind(self):
        """
        审查 重后加字
        :return str/None:  返回错误信息, 字符合法返回None
        """
        if self.__result[6] is not None:
            if self.__result[6] not in ["ད", 'ས']:
                return ("不存在重后加字(ཡང་འཇུག་): {}".format(self.__result[6]))
            else:
                if self.__result[6] == "ད":
                    if self.__result[5] not in ["ན", "ར", "ལ"]:
                        return ("重后加字(ཡང་འཇུག་) ད 使用不当，属于非法字符")
                if self.__result[6] == "ས":
                    if self.__result[5] not in ["ག", "ང", "བ", "མ"]:
                        return ("重后加字(ཡང་འཇུག་) ས 使用不当，属于非法字符")

    #############################################################################
    # 外调功能函数群组
    
    def front(self):
        """
        :return str: སྔོན་འཇུག་ 获取前加字
        """
        self.__analysis()
        return self.__result[0]

    def top(self):
        """
        :return str: མགོ་ཅན་ 获取上加字
        """
        self.__analysis()
        return self.__result[1]

    def basic(self):
        """
        :return str: མིང་གཞི་ 获取基字
        """
        self.__analysis()
        return self.__result[2]

    def below(self):
        """
        :return str: འདོགས་ཅན་ 下加字
        """
        self.__analysis()
        return self.__result[3]

    def symbol(self):
        """
        :return str: དབྱངས་  音标
        """
        self.__analysis()
        return self.__result[4]

    def behind(self):
        """
        :return str: རྗེས་འཇུག་ 后加字
        """
        self.__analysis()
        return self.__result[5]

    def repeat_behind(self):
        """
        :return str: ཡང་འཇུག་ 重后加字
        """
        self.__analysis()
        return self.__result[6]

    def get_all(self):
        """
        :return list: 元素映射表：[前加字, 上加字, 基字, 下加字, 后加字, 重后加字]
        """
        self.__analysis()
        return self.__result

    def is_right(self):
        """
        根据正字规范，判断词的合法性
        :return : 返回错误信息 
        """
        # 1.分析字符串 并填充 信息到数组
        self.__analysis()
        # 2.将审查信息集存进一个 list 中
        results = [self.__check_front(), self.__check_top(), self.__ckeck_under(),
                   self.__check_behind(), self.__check_repeat_behind()]
        # 3.观察列表
        state = True                                # 用于存储 list 元素信息
        for result in results:
            if result != None:
                state = False                       # 只要其中一个不是None将状态值切换并，跳出循环
                break
        # 4. 处理列表
        data = ["该字符"]                          # 存储 反馈信息
        if state == False:                          # 若 state 为 False，则字符存在 非法元素
            for result in results:
                if result != None:                 # 过滤 None
                    data.append(result)
        else:
            data.append("合法！")

        # 5.制作函数返回值 - 此处采用策略：转成str、并去掉list和str的边框
        return str(data)[1:-1].replace("'", '').replace(",", "---")

class Auxiliary_Word():
    """
    助词分析类
    1. 只能处理 依据助词前词语的后加字和重后加字，按照规则严格选取的助词  无法分析依据语义选取的助词
    2. 无法排除文中 不作为助词的助词词汇  比如 དེ་  总会认为是连引助词进行处理和判断，而有时候他在文中并不作为助词，而是词语的组成部分部分
    3. 因为元字符做了预处理 将空格删掉了 如此无法通过空格判断一些句子关系，若保留空格，不规则的元字符将会对本程序造成很大的干扰
    4. 对目标字符的要求是 必须严格遵守藏文词语结构，带有词终结符表明词域，若文中带有句终结符和段落终结符，不会对程序造成干扰
    5. 可以按输出分析结果需求的不同 修改 analysis() 
    """

    def __init__(self, str_):
        self.__meta_str = str_     # 元数据

        # 每次创建新的实例一下数据都需要 重置为空
        self.__sub_str = ''                      # 元数据 经过滤的  子串
        self.__keys_info_in_meta_str = {}        # 助词在 元字符串里的 索引信息
        self.__keys_info_in_sub_str = {}         # 助词在 子串里的 索引信息
        self.__keys_front_info_in_sub_str = {}   # 助词 和 前项词在 子串中的 索引信息

        self.__make_ready_data()   # 只要创建实例  自动制作备用数据
    ################################################################################## 内调公共数据区
    # 稳定的数据  只可以遍历，不能在方法内对其做编辑

    # འབྲེལ་སྒྲ་ བྱེད་སྒྲ་
    __possessives_keys = ["་གི་", "་ཀྱི་", "་གྱི་", "་ཡི་", "འི་",
                          "་གིས་", "་ཀྱིས་", "་གྱིས་", "་ཡིས་"]
    # སླར་བསྡུ་
    __final_keys = ["་གོ་", "་ངོ་", "་དོ་", "་ནོ་", "་བོ་", "་མོ་",
                    "་འོ་", "་རོ་", "་ལོ་", "་སོ་", "་ཏོ་"]
    # རྒྱན་སྡུད་
    __conversion_keys = ["་ཀྱང་", "་ཡང་", "་འང་"]
    # ལ་དོན་  因为嵌入在词语里无法分辨了 ན་ལ་规则模糊
    __judging_position_keys = ["་སུ་", "་ཏུ་", "་དུ་", "་རུ་"]
    # ལྷག་བཅས་
    __extended_keys = ["་ཏེ་", "་སྟེ་", "་དེ་"]
    # འབྱེད་སྡུད་
    __question_keys = ["་གམ་", "་ངམ་", "་དམ་", "་ནམ་", "་བམ་",
                       "་མམ་", "་འམ་", "་རམ་", "་ལམ་", "་སམ་", "་ཏམ་"]
    # བདག་སྒྲ་  མ་དང་མོ་ 表女性，无规则限制
    __host_word_keys = ["་པ་", "་བ་", "་པོ་"]
    # ཚིག་ཕྲད་ཞིང་སོགས་
    __conjunction_keys = ["་ཞིང་", "་ཞེས་", "་ཞེའོ་", "་ཞེ་ན་", "་ཞིག་", "་ཅིང་", "་ཅེས་",
                          "་ཅེའོ་", "་ཅེ་ན་", "་ཅིག་", "་ཤིང་", "་ཤེའོ་", "་ཤེ་ན་", "་ཤིག་"]
    # 保留字的表、 用于筛选其他标点符号等干扰符号
    __is_word = ['ཀ', 'ཁ', 'ག', 'ང', 'ཅ', 'ཆ', 'ཇ', 'ཉ', 'ཏ', 'ཐ', 'ད', 'ན', 'པ', 'ཕ',
                 'བ', 'མ', 'ཙ', 'ཚ', 'ཛ', 'ཝ', 'ཞ', 'ཟ', 'འ', 'ཡ', 'ར', 'ལ', 'ཤ', 'ས', 'ཧ', 'ཨ',
                 'ྐ',   'ྑ',   'ྒ',   'ྔ',   'ྕ',   'ྖ',   'ྗ',   'ྙ',  'ྟ',   'ྠ',   'ྡ',   'ྣ',   'ྤ',   'ྥ',
                 'ྦ',   'ྨ',   'ྩ',   'ྪ',   'ྫ',   'ྮ',   'ྯ',   'ྰ',   'ྴ',   'ྶ',   'ྷ',   'ྸ',
                 'ི',  'ུ',  'ེ', 'ོ',  'ཽ',  'ྀ',  'ཻ',   '྄',  '༷',  '༵',
                 'ྱ', 'ྲ', 'ླ',  'ྭ',  'ྰ',  '་',  '࿆',  '༘',  '༙',  'ྼ',  'ྻ', "།",
                 'ཀྵ',  'ཊ',  'ཋ',  'ཌ',  'ཎ',  'ཥ',
                 'ཱི',  'ཱྀ',  'ཱུ',  'ྲྀ',  'ཷ',  'ླྀ',  'ཹ']

   # 助词 全集
    __all_keys = (__possessives_keys + __final_keys + __conversion_keys + __judging_position_keys + __extended_keys
                  + __question_keys + __conjunction_keys + __host_word_keys)

    ######################################################################## 内调功能函数区，供类内部函数调用，外部不可见，无法调用
    # 中间缓存 用完重置为空
    __process_str = ''                  # 缓存 -- 用于组装字符的
    __s_list = []                       # 缓存 -- 用于取目标字符的缓存
    __start = 0                         # 缓存 -- 初始化起始值
    # 制作各项准备数据
   
    def __make_ready_data(self):
        """
        制作各项准备数据
        """
        # 1 .对元数据进行过滤
        for word in self.__meta_str:
            if word in self.__is_word:
                self.__sub_str = self.__sub_str + word

        # 2. 记录助词在 元字符串里的信息
        for key in self.__all_keys:
            if self.__sub_str.count(key) > 0:
                for i in range(self.__meta_str.count(key)):             # 不能查到一个该关键就停止查询，
                    index = self.__meta_str.find(
                        key, self.__start+1)   # 记录第一次查到该关键词查找位置
                    self.__start = self.__meta_str.find(
                        key, self.__start+1)   # 更新 查询起始位置
                    self.__keys_info_in_meta_str[index] = key
                # 按照 助词的索引值排序，保证 按从左到右输出修改建议 对应点的标识为以 1 开始的升序
                self.__keys_info_in_meta_str = dict(
                    sorted(self.__keys_info_in_meta_str.items()))
                self.__start = 0                               # 当前key工作完 重置起始参数

        # 3. 记录助词在 子串里的信息
        for key in self.__all_keys:
            if self.__sub_str.count(key) > 0:
                for i in range(self.__sub_str.count(key)):    # 不能查到一个该关键就停止查询，
                    index = self.__sub_str.find(
                        key, self.__start+1)   # 记录第一次查到该关键词查找位置
                    self.__start = self.__sub_str.find(
                        key, self.__start+1)   # 更新 查询起始位置
                    self.__keys_info_in_sub_str[index] = key
                # 按照 助词的索引值排序，保证 按从左到右输出修改建议 对应点的标识为以 1 开始的升序
                self.__keys_info_in_sub_str = dict(
                    sorted(self.__keys_info_in_sub_str.items()))
                self.__start = 0                               # 当前 key 工作完 重置起始参数

        # 4. 取出待处理 助词前项词 并制作 助词和前项词在 字串中的位置信息  其中key值为 助词的index
        for key, value in self.__keys_info_in_sub_str.items():
            for index in range(key-10, key):                # 合法的最长字为 9
                self.__s_list.append(self.__sub_str[index])
                # 目标字集缓存  去掉最后一项 词终结符，即助词前的终结符  倒序为了便于遍历
                cache = list(reversed(self.__s_list[:-1]))

            # 使用基于逆序缓存取到的index 在正序缓存中 得到目标子串(list)
            goal_str = (self.__s_list[(-cache.index("་")-1):])
            for i in range(len(goal_str)):
                self.__process_str = self.__process_str + \
                    (goal_str[i])   # 将 缓存中的字符 整合成一个字符串 并将变量重定向到该字符串

            self.__keys_front_info_in_sub_str[key] = self.__process_str, value
            self.__process_str = ''  # 缓存重置成空
            self.__s_list = []  # 缓存重置成空

    def __check_possessives_keys(self, info):
        """
        འབྲེལ་སྒྲ་ བྱེད་སྒྲ་ 检查  属格、具格关键词    程序只能根据规则建议两个关键词可选项，具体使用属格或具格需要文字编撰人员视文意而定。
        :param info [str, str]: 前项词和 助词 对
        :return str/True: 如果助词使用有误，返回修改建议，具体选用属格或具格得依据语义。 如果用词正确返回 True
        """
        def advice(key):
            """
            根据助词使用规则，给出建议
            :param keys: 前项字
            :return str: 建议使用的 助词
            """
            if key in ["ད", "བ", "ས"]:
                return "(ཀྱི་ / ཀྱིས་)"
            if key in ["ག", "ང"]:
                return "(གི་ / གིས་)"
            if key in ["ན", "མ", "ར"]:
                return "(གྱི་ / གྱིས་)"
            if key in ["འ", None]:
                return "(ཡི་ / ཡིས་)"

       # 排除句终结符和段落终结符的干扰
        if "།" in info[0]:
            single_words = info[0][::-1]   # 倒序切片 因为有可能存在 段落终结符 即为两个句终结符
            for single_word in single_words:
                if single_word == "།":  # 若存在 终结符
                    index = single_words.index(single_word)
                    front_word = single_words[:index:-1]
                    word = Word(front_word)
                    keys = word.get_all()  # 提取前项词的 组成元素
                    break
        else:  # 不存在句终结符
            word = Word(info[0])
            keys = word.get_all()  # 提取前项词的 组成元素
        auxiliary_word = info[1]         # 助词

        # 取到前项词的最后一项 可能是后加字 也可能是重后加字
        if keys[-1] == None:
            key = keys[-2]
        else:
            key = keys[-1]

        if auxiliary_word in ["་གི་", "་གིས་"]:
            if key not in ["ག", "ང"]:
                return advice(key)  # 返回修改建议
            else:
                return True
        elif auxiliary_word in ["་ཀྱི་", "་ཀྱིས་"]:
            if key not in ["ད", "བ", "ས"]:
                return advice(key)
            else:
                return True
        elif auxiliary_word in ["་གྱི་", "་གྱིས་"]:
            if key not in ["ན", "མ", "ར"]:
                return advice(key)
            else:
                return True
        elif auxiliary_word in ["་ཡི་", "་ཡིས་"]:
            if key in ["འ"] or key == None:
                return True
            else:
                return advice(key)
            
        
    def __check_final_keys(self, info):
        """
        སླར་བསྡུ་ 检查语终词
        :param info: 前项词和 助词 对
        :return str/True: 如果助词使用有误，返回修改建议。 如果用词正确返回 True  
        """
        def advice(keys):
            """
            根据助词使用规则，给出建议
            :param keys<list>: 前项词的 元素映射表 
            :return <str>: 建议使用的 助词
            """
            if keys[-1] != None:
                if keys[-1] == "ད":
                    return "ཏོ་"
                if keys[-1] == "ས":
                    return "སོ་"
            else:
                if keys[-2] != None:

                    return keys[-2]+"ོ་"
                else:
                    return "འོ་"

        # 排除句终结符和段落终结符的干扰
        if "།" in info[0]:
            single_words = info[0][::-1]   # 倒序切片 因为有可能存在 段落终结符 即为两个句终结符
            for single_word in single_words:
                if single_word == "།":  # 若存在 终结符
                    index = single_words.index(single_word)
                    front_word = single_words[:index:-1]
                    word = Word(front_word)
                    keys = word.get_all()  # 提取前项词的 组成元素
                    break
        else:  # 不存在句终结符
            word = Word(info[0])
            keys = word.get_all()  # 提取前项词的 组成元素
        auxiliary_word = info[1]         # 助词

        if advice(keys) != auxiliary_word:
            return "({})".format(advice(keys))
        else:
            return True

    def __check_conversion_keys(self, info):
        """
        རྒྱན་སྡུད་  检查转合词
        :param info: 前项词和 助词 对
        :return str/True: 如果助词使用有误，返回修改建议。 如果用词正确返回 True  
        """
        def advice(keys):
            """
            根据助词使用规则，给出建议
            :param keys<list>: 前项词的 元素映射表
            :return <str>: 建议使用的 助词
            """
            if keys[-1] != None:
                return "ཀྱང་"
            if keys[-1] == None:
                if keys[-2] != None:
                    if keys[-2] in ["ག", "ད", "བ", "ས"]:
                        return "ཀྱང་"
                    if keys[-2] in ["ང", "ན", "མ", "ར", "ལ"]:
                        return "ཡང་"
                    if keys[-2] == "འ":
                        return "--འང་ / ཡང་"
                if keys[-2] == None:
                    return "--འང་ / ཡང་"
       # 排除句终结符和段落终结符的干扰
        if "།" in info[0]:
            single_words = info[0][::-1]   # 倒序切片 因为有可能存在 段落终结符 即为两个句终结符
            for single_word in single_words:
                if single_word == "།":  # 若存在 终结符
                    index = single_words.index(single_word)
                    front_word = single_words[:index:-1]
                    word = Word(front_word)
                    keys = word.get_all()  # 提取前项词的 组成元素
                    break
        else:  # 不存在句终结符
            word = Word(info[0])
            keys = word.get_all()  # 提取前项词的 组成元素
        auxiliary_word = info[1]         # 助词
        del word  # 回收对象
        if advice(keys) != auxiliary_word:
            return "({})".format(advice(keys))
        else:
            return True

    def __check_judging_position_keys(self, info):
        """
        ལ་དོན་ 检查 判位助词
        :param info: 前项词和 助词 对
        :return str/True: 如果助词使用有误，返回修改建议。 如果用词正确返回 True  
        """
        def advice(keys):
            """
            根据助词使用规则，给出建议
            :param keys<list>: 前项词的 元素映射表
            :return <str>: 建议使用的 助词
            """
            if keys[-1] != None:
                return "ཏུ་"
            if keys[-1] == None:
                if keys[-2] != None:
                    if keys[-2] in ["ག", "བ"]:
                        return "ཏུ་"
                    if keys[-2] in ["ང", "ད", "ན", "མ", "ར", "ལ"]:
                        return "དུ་"
                    if keys[-2] == "འ":
                        return "--ར་ / རུ་"
                if keys[-2] == None:
                    return "--ར་ / རུ་"

        # 排除句终结符和段落终结符的干扰
        if "།" in info[0]:
            single_words = info[0][::-1]   # 倒序切片 因为有可能存在 段落终结符 即为两个句终结符
            for single_word in single_words:
                if single_word == "།":  # 若存在 终结符
                    index = single_words.index(single_word)
                    front_word = single_words[:index:-1]
                    word = Word(front_word)
                    keys = word.get_all()  # 提取前项词的 组成元素
                    break
        else:  # 不存在句终结符
            word = Word(info[0])
            keys = word.get_all()  # 提取前项词的 组成元素
        auxiliary_word = info[1]         # 助词
        del word  # 回收对象
        if advice(keys) != auxiliary_word:
            return "({})".format(advice(keys))
        else:
            return True

    def __check_extended_keys(self, info):
        """
        ལྷག་བཅས་  检查 连引助词
        :param info: 前项词和 助词 对
        :return str/True: 如果助词使用有误，返回修改建议。 如果用词正确返回 True  
        """
        def advice(keys):
            """
            根据助词使用规则，给出建议
            :param keys<list>: 前项词的 元素映射表
            :return <str>: 建议使用的 助词
            """
            if keys[-1] != None:
                return "ཏེ་"
            if keys[-1] == None:
                if keys[-2] != None:
                    if keys[-2] in ["ད"]:
                        return "དེ་"
                    if keys[-2] in ["ག", "ང", "བ", "མ", "འ"]:
                        return "སྟེ་"
                    if keys[-2] in ["ན", "ར", "ལ", "ས"]:
                        return "ཏེ་"
                if keys[-2] == None:
                    return "སྟེ་"

        # 排除句终结符和段落终结符的干扰
        if "།" in info[0]:
            single_words = info[0][::-1]   # 倒序切片 因为有可能存在 段落终结符 即为两个句终结符
            for single_word in single_words:
                if single_word == "།":  # 若存在 终结符
                    index = single_words.index(single_word)
                    front_word = single_words[:index:-1]
                    word = Word(front_word)
                    keys = word.get_all()  # 提取前项词的 组成元素
                    break
        else:  # 不存在句终结符
            word = Word(info[0])
            keys = word.get_all()  # 提取前项词的 组成元素
        auxiliary_word = info[1]         # 助词
        del word  # 回收对象
        if advice(keys) != auxiliary_word:
            return "({})".format(advice(keys))
        else:
            return True

    def __check_question_keys(self, info):
        """
        འབྱེད་སྡུད་  检查疑问离合 助词
        :param info: 前项词和 助词 对
        :return str/True: 如果助词使用有误，返回修改建议。 如果用词正确返回 True  
        """
        def advice(keys):
            """
            根据助词使用规则，给出建议
            :param keys<list>: 前项词的 元素映射表 
            :return <str>: 建议使用的 助词
            """
            if keys[-1] != None:
                if keys[-1] == "ད":
                    return "ཏམ་"
                if keys[-1] == "ས":
                    return "སམ་"
            else:
                if keys[-2] != None:

                    return keys[-2] + "མ་"
                else:
                    return "འམ་"

        # 排除句终结符和段落终结符的干扰
        if "།" in info[0]:
            single_words = info[0][::-1]   # 倒序切片 因为有可能存在 段落终结符 即为两个句终结符
            for single_word in single_words:
                if single_word == "།":  # 若存在 终结符
                    index = single_words.index(single_word)
                    front_word = single_words[:index:-1]
                    word = Word(front_word)
                    keys = word.get_all()  # 提取前项词的 组成元素
                    break
        else:  # 不存在句终结符
            word = Word(info[0])
            keys = word.get_all()  # 提取前项词的 组成元素
        auxiliary_word = info[1]         # 助词
        if advice(keys) != auxiliary_word:
            return "({})".format(advice(keys))
        else:
            return True

    def __check_host_key(self, info):
        """
        བདག་སྒྲ་  检查 表人助词  
        :param info: 前项词和 助词 对
        :return str/True: 如果助词使用有误，返回修改建议。 如果用词正确返回 True  
        """
        def advice(keys):
            """
            根据助词使用规则，给出建议
            :param keys<list>: 前项词的 元素映射表 
            :return <list>: 建议使用的 助词选项(选项内元素都合法，具体看使用者选择)
            """
            if keys[-1] != None:
                return ['པ་', 'པོ་']
            else:
                if keys[-2] != None:
                    if keys[-2] in ["ག", "ད", "ན", "བ", "མ", "ས"]:
                        return ['པ་', 'པོ་']
                    if keys[-2] in ["ང", "འ", "ར", "ལ"]:
                        return ['པ་', 'བ་']
                else:
                    return ['པ་', 'བ་']

        # 排除句终结符和段落终结符的干扰
        if "།" in info[0]:
            single_words = info[0][::-1]   # 倒序切片 因为有可能存在 段落终结符 即为两个句终结符
            for single_word in single_words:
                if single_word == "།":  # 若存在 终结符
                    index = single_words.index(single_word)
                    front_word = single_words[:index:-1]
                    word = Word(front_word)
                    keys = word.get_all()  # 提取前项词的 组成元素
                    break
        else:  # 不存在句终结符
            word = Word(info[0])
            keys = word.get_all()  # 提取前项词的 组成元素

        # 助词  需要去除 字符串首的词终结符
        auxiliary_word = info[1][1:]
        if (keys[-1] == None) and (keys[-2] in ["ང", "འ", "ར", "ལ", None]):
                # 将 修改建议 整理成统一输出样式
            return ("({})".format(str(advice(keys)).replace("[", "").replace("]", "").replace("'", "").replace(",", "/"))
                    + "如果词语总数量为奇数：请选用 བ -- 如果为偶数：请选用 པ -- 例如 ལྷ་ས་བ་  མདའ་པ་")
        else:
            if auxiliary_word not in advice(keys):
                return ("({})".format(str(advice(keys)).replace("[", "").replace("]", "").replace("'", "").replace(",", "/")))
            else:
                return True

    def __checkz_conjunction_keys(self, info):
        """
        ཚིག་ཕྲད་ཞིང་སོགས་  连词 
        :param info: 前项词和 助词 对
        :return str/True: 如果助词使用有误，返回修改建议。 如果用词正确返回 True  
        """
        def advice(keys):
            """
            根据助词使用规则，给出建议
            :param keys<list>: 前项词的 元素映射表 
            :return <list>: 建议使用的 助词选项(选项内元素都合法，具体看使用者选择)
            """
            if keys[-1] != None:
                if keys[-1] == "ད":
                    return ["ཅིང་", "ཅེས་", "ཅེའོ་", "ཅེ་ན་",  "ཅིག་"]
                if keys[-1] == "ས":
                    return ["ཤིང་", "ཞེས་", "ཤེའོ་", "ཤེ་ན་", "ཤིག་"]
            else:
                if keys[-2] != None:
                    if keys[-2] in ["ག", "ད", "བ"]:
                        return ["ཅིང་", "ཅེས་", "ཅེའོ་", "ཅེ་ན་",  "ཅིག་"]
                    if keys[-2] in ["ང", "འ", "ར", "ལ", "མ", "ན"]:
                        return ["ཞིང་", "ཞེས་", "ཞེའོ་", "ཞེ་ན་", "ཞིག་"]
                    if keys[-2] == "ས":
                        return ["ཤིང་", "ཞེས་", "ཤེའོ་", "ཤེ་ན་", "ཤིག་"]
                else:
                    return ["ཞིང་", "ཞེས་", "ཞེའོ་", "ཞེ་ན་", "ཞིག་"]

        # 排除句终结符和段落终结符的干扰
        if "།" in info[0]:
            single_words = info[0][::-1]   # 倒序切片 因为有可能存在 段落终结符 即为两个句终结符
            for single_word in single_words:
                if single_word == "།":  # 若存在 终结符
                    index = single_words.index(single_word)
                    front_word = single_words[:index:-1]
                    word = Word(front_word)
                    keys = word.get_all()  # 提取前项词的 组成元素
                    break
        else:  # 不存在句终结符
            word = Word(info[0])
            keys = word.get_all()  # 提取前项词的 组成元素
        auxiliary_word = info[1][1:]         # 助词  需要去除 字符串首的词终结符
        if auxiliary_word not in advice(keys):
            # 将 修改建议 整理成统一输出样式
            return "({})".format(str(advice(keys)).replace("[", "").replace("]", "").replace("'", "").replace(",", "/"))
        else:
            return True

    ######################################################################### 外调功能函数区， 供实例对象调用的功能函数

    def analysis(self):
        """
        分析中心, 调用各个分析分支方法，生成总分析结果
        :return str/True: 修改信息：助词使用有误则在子串中标出错误位置，并给出对应的修改建议  / 如没有错误返回 True
        """
        ############## 1. 收集 修改信息 -- 枚举所有 助词类型，并分别处理
        no = 1    # 记录一下处理次序  也可以作为 标识使用
        result = {}
        for key, value in self.__keys_front_info_in_sub_str.items():
            # འབྲེལ་སྒྲ་ བྱེད་སྒྲ་  属格、具格关键词 处理入口
            if value[1] in self.__possessives_keys:
                advice = self.__check_possessives_keys(value)  # 得到当前的修改建议
                if advice != True:
                    result[no] = key, advice
                    no += 1
            # སླར་བསྡུ་  语终词 处理入口
            if value[1] in self.__final_keys:
                advice = self.__check_final_keys(value)
                if advice != True:
                    result[no] = key, advice
                    no += 1
            # རྒྱན་སྡུད་  转合词 处理入口
            if value[1] in self.__conversion_keys:
                advice = self.__check_conversion_keys(value)
                if advice != True:
                    result[no] = key, advice
                    no += 1
            # ལ་དོན་ 判位词 处理入口
            if value[1] in self.__judging_position_keys:
                advice = self.__check_judging_position_keys(value)
                if advice != True:
                    result[no] = key, advice
                    no += 1
            # ལྷག་བཅས་ 连引词 处理入口
            if value[1] in self.__extended_keys:
                advice = self.__check_extended_keys(value)
                if advice != True:
                    result[no] = key, advice
                    no += 1
            # འབྱེད་སྡུད་  疑问离合助词 处理入口
            if value[1] in self.__question_keys:
                advice = self.__check_question_keys(value)
                if advice != True:
                    result[no] = key, advice
                    no += 1
            # བདག་སྒྲ་  表人助词 处理入口
            if value[1] in self.__host_word_keys:
                advice = self.__check_host_key(value)
                if advice != True:
                    result[no] = key, advice
                    no += 1
            # ཚིག་ཕྲད་ཞིང་སོགས་  连词处理入口
            if value[1] in self.__conjunction_keys:
                advice = self.__checkz_conjunction_keys(value)
                if advice != True:
                    result[no] = key, advice
                    no += 1
        # 按照 助词的索引值排序，保证 按从左到右输出修改建议 对应点的标识为以 1 开始的升序
        # 按照原索引值 做升序排列 以免元字符串混乱
        result = dict(sorted(result.items(), key=lambda item: item[1][0]))

        #################### 2. 输出结果  这里的输出策略是：在子串中标出可疑非法使用的主持，并按序列对应映射地将助词修改信息罗列出 
        list_str = list(self.__sub_str)   # 字符串 修改成 list 便于插入修改信息
        i = 0                             # 每插入一项 原索引值后移一项 第一次插入不需后移
        return_list = []                  # 修改建议
        if len(list(result.items())) != 0:
            for key, value in result.items():
                list_str.insert(i+value[0]+1, "[{}]".format(str(key)))
                i += 1
                return_list.append((key, value[1]))  # 修改建议

            result_str = "SENTENCE: \n" + ''.join(list_str)          # 原子串 修改位置
            return_str = ''
            for info in return_list:
                return_str = return_str + '\n' + \
                    str(info)[1:][:-1].replace("'",
                                               "").replace(",", ":")  # 修饰一下输出样式
            return result_str + "\n\nADVICE:" + return_str
        else:
            return True

        # 助词信息 分析能力有限 仅能对规则严明的助词进行合法性分析，对根据语义选择或者存在多选择项时，只能靠人工选择


if __name__ == '__main__':
    pass

