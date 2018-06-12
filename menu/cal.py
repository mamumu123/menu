from pulp import *
from copy import deepcopy
import json
import csv


# 加载JSON数据
def loadJson(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


#
def addToDict(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a: {key_b: val}})


# 套餐中单品的数量

def num_sin(upDict, m, s):
    # 如果是套餐，
    if m[0] == 'M':
        # 如果套餐中有这个单品   #有一些单品在所有套餐中都不出现
        if s in upDict[m]:
            # print(m, s, upDict[m][s])
            return int(upDict[m][s])
        # 如果没有
        else:
            return 0
    # 如果不是套餐
    else:
        # 只有该单品返回1，其他都是0
        if m == s:
            # print('+1')
            return 1
        else:
            return 0


# 增加一个菜品，能够得到的最低值
def add_cal(single):
    _single = deepcopy(single)  # 顾客所点的菜品（根据要求，事先处理为单菜品）
    rFile = open('./data/single.csv', "r", encoding='utf-8')
    dataLine = rFile.readline()
    lineCount = 0
    all_single = []
    all_single_el = []
    while dataLine:
        lineCount += 1
        if lineCount != 1:
            line = dataLine.strip().split('\t')
            all_single.append(line[0])
            all_single_el.append(line)
        dataLine = rFile.readline()
    # print(_single)
    #print(all_single_el)
    target_min = 9999999
    target_list = []
    target_single = ''
    for item in all_single_el:
        add_single = deepcopy(_single)
        if item[0] in add_single:
            add_single[item[0]] += 1
        else:
            add_single[item[0]] = 1
        cal_cost, cal_zuhe = cal(add_single)
        if (cal_cost < target_min):
            target_min = cal_cost
            target_list = cal_zuhe
            target_single = item
        # print(cal_cost)
    # print('min', target_min)
    # print(target_list)
    #print('target_single', target_single)
    return target_single, target_min, target_list


# 在这个函数中计算
def cal(single):
    # 最低值，初始化为0
    result = 0
    #######预处理####################################
    _single = deepcopy(single)  # 顾客所点的菜品（根据要求，事先处理为单菜品）
    prices = loadJson('./data/priceDict.json')  # 价格
    Ingredients = [pr for pr in prices]  # 成分 ：所有的菜品，包括套餐和单菜
    # inforMatrix
    rFile = open('./data/inforMatrix.csv', "r", encoding='utf-8')
    # 处理矩阵，得到upDict[套餐][单菜]=num
    upDict = {}
    # 一行一行处理
    inforMatrixLine = rFile.readline()
    inforLineCount = 0
    while inforMatrixLine:
        # 行数
        inforLineCount += 1
        # 如果是第一行，则为表头，单独处理
        if (inforLineCount == 1):
            singleList = inforMatrixLine.strip().split(',')[1:]
        # 否则
        else:
            taocan = inforMatrixLine.strip().split(',')
            # 套餐名字
            taocan_name = taocan[0]
            # 套餐包含的单品数量
            taocan_sin = taocan[1:]
            # 对于每一个单品
            for index in range(len(taocan_sin)):
                # 将单品加入套餐信息中
                # 参数，套餐字典 ,套餐名，单品名，单品数量
                addToDict(upDict, taocan_name, singleList[index], taocan_sin[index])

        inforMatrixLine = rFile.readline()
    # print(upDict)
    ######         开始做线性规划        ###############################
    # 创建问题实例，求最小极值
    prob = LpProblem("The Whiskas Problem", LpMinimize)
    # 构建Lp变量字典，变量名以Ingr开头，如Ingr_CHICKEN，下界是0
    # , cat='LpInteger'
    ingredient_vars = LpVariable.dicts("Ingr", Ingredients, 0, cat='Integer')
    # 添加目标方程x`
    #     min(price(i)*num(i))
    prob += lpSum([prices[i] * ingredient_vars[i] for i in Ingredients])
    # 约束条件  所有菜品中的对应单菜数量加起来要和顾客要求的数量一致
    # 即顾客点了多少个单菜，就有多少个限制条件
    for sin in _single:
        # 顾客点的该单菜=菜品数量*(该菜品中含有的该单菜数量）
        # num_sin():该菜品中含有的该单菜数量
        # ingredient_vars[per]:菜品数量
        # _single[sin]：顾客点的该单菜的数量
        prob += lpSum([num_sin(upDict, per, sin) *
                       ingredient_vars[per] for per in Ingredients]) == int(_single[sin])
        #
    # 求解
    prob.solve()
    zuhe = {}
    for v in prob.variables():
        if v.varValue != 0:
            name = v.name[5:]
            result += float(v.varValue) * prices[name]
            zuhe[name] = int(v.varValue)
    return result, zuhe


## 该函数用于把所有的套餐都变成单品
def chuli(input):
    # 该函数用于把所有的套餐都变成单品
    _input = deepcopy(input)
    # print('input', _input)
    M_in = {}
    S_in = {}
    # 对于每一个输入，先进行分类
    for per in _input:
        # 如果是套餐，放入套餐字典
        if per[0] == 'M':
            M_in[per] = _input[per]
        # 如果不是套餐，放入单品字典
        else:
            S_in[per] = _input[per]
    infoDict = loadJson('./data/inforDict.json')
    # 将套餐字典中的单品数量都加到单品字典中
    for item in M_in:
        info = infoDict[item]
        # print(info)
        for single in info:
            if single in S_in:
                S_in[single] += info[single] * M_in[item]
            else:
                S_in[single] = info[single] * M_in[item]
    # print(S_in)
    return S_in


if __name__ == '__main__':
    # 引入input
    data = loadJson('./data/trial_data.json')
    trial = data.get('trial')
    for index in range(len(trial)):
        input = trial[index]['input']
        # 将所有的菜品都转换为单品
        single = chuli(input)
        # # 线性规划计算
        cal_cost, cal_zuhe = cal(single)
        print('第' + str(index) + '个测试:')
        print('通过线性规划，得到的最小价格和组合分别为：\ncost：', cal_cost, '\noutput：', cal_zuhe)
        infoDict = loadJson('./data/inforDict.json')
        output = trial[index]['output']
        cost = trial[index]['cost']

        print('real', cost)
        print('real_output\n', output)
