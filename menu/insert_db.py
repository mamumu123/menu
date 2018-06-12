import sqlite3
import pandas as pd

# 此文件的作用为将数据插入到数据库
if __name__ == '__main__':
    # 连接数据库
    fileName = ['./data/single.csv', './data/combo.csv']
    conn = sqlite3.connect("./db/menu.db")
    #######################################################################
    # 单菜品处理
    # 读取single
    df = pd.read_csv(fileName[0], sep='\t')
    # 插入到数据库
    df.to_sql('tbSingle', conn, if_exists='replace', index=False)
    ###################################################################################
    # 处理tbMulti
    rFile = open(fileName[1], "r", encoding='utf-8')
    targetFile = './data/tem_1.csv'
    targetFile_el = './data/tem_2.csv'
    wFile = open(targetFile, "w", encoding='utf-8')
    wFile_el = open(targetFile_el, "w", encoding='utf-8')
    # 一行行读取，需要对原始数据做处理后，再插入数据库
    dataLine = rFile.readline()  # 读取一行数据
    line = ''
    line_el = ''
    line_count = 0
    while dataLine:
        # 将每一行中的数据拆分
        dataList = dataLine.split("\t")
        # 得到tbMulti中需要的数据
        line = line + dataList[0] + '\t' + dataList[1] + '\t' + dataList[2] + '\n'
        dataLine = rFile.readline()
    wFile.write(line)
    wFile.close()
    rFile.close()
    df = pd.read_csv(targetFile, sep='\t')
    # 插入到数据库
    df.to_sql('tbMulti', conn, if_exists='replace', index=False)
    # ##############################################################################
    # 处理tbMultiElement
    rFile = open(fileName[1], "r", encoding='utf-8')
    dataLine = rFile.readline()  # 读取一行数据
    while dataLine:
        line_count += 1
        # 表头数据
        if line_count == 1:
            line_el = 'Mid\t' + 'Sid\t' + 'Snum\n'
        # 得到tbMultiElement需要的数据
        else:
            dataList = dataLine.split("\t")
            Mid = dataList[0]
            s_el = dataList[3].split('+')
            for i in range(len(s_el)):
                tt = s_el[i].split(',')
                line_el += Mid + '\t' + tt[0] + '\t' + tt[1] + '\n'
        dataLine = rFile.readline()
    # print(line_el)
    wFile_el.write(line_el)
    wFile_el.close()
    rFile.close()
    df = pd.read_csv(targetFile_el, sep='\t')
    # 将套餐中的单菜品信息，插入数据库
    df.to_sql('tbMultiElement', conn, if_exists='replace', index=False)
    conn.close()
