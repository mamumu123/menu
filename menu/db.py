import sqlite3


# 检查用户是否存在，及密码是否正确
def check_user(username, password):
    conn = sqlite3.connect('./db/menu.db')
    username = '"' + username + '"'
    # 查询该用户信息
    sql = """select * from tbUser where Pname like %s"""
    query = conn.execute(sql % username)
    result = query.fetchall()
    conn.close()
    # 如果不存在该用户
    if result == []:
        return None
    # 返回该用户信息
    return result[0]


# 插入单菜品
def insertmen(data):
    # 解析出相关信息
    _data = data[:]
    _ID = '"' + str(_data[0]) + '"'
    _name = '"' + str(_data[1]) + '"'
    _price = float(_data[2])
    # print(_ID, '   ', _name, '   ', _price)
    conn = sqlite3.connect('./db/menu.db')
    sql = """insert into tbSingle values(%s,%s,%f)"""
    conn.execute(sql % (_ID, _name, _price))
    conn.commit()
    conn.close()


# 插入套餐菜品
# 先提交到tbMulti
# 再讲具体单菜品信息提交到tbMultiElement
def insertMul(data):
    conn = sqlite3.connect('./db/menu.db')
    # 解析出相关信息
    _data = data[:]
    _ID = '"' + str(_data[0]) + '"'
    _name = '"' + str(_data[1]) + '"'
    _price = float(_data[3])
    _mixList = str(_data[2]).strip().split(' ')
    # print(_ID, '   ', _name, '   ', _price, "", _mixList)
    # 提交到总套餐
    sql = """insert into tbMulti values(%s,%s,%f)"""
    conn.execute(sql % (_ID, _name, _price))
    conn.commit()
    # 组成提交
    for i in range(len(_mixList)):
        _mix = _mixList[i].split('*')
        _mix_ID = '"' + _mix[0].split('￥')[0] + '"'
        _mix_num = int(_mix[1])
        # print(_mix, _mix_ID, _mix_num)
        sql = """insert into tbMultiElement values(%s,%s,%d)"""
        conn.execute(sql % (_ID, _mix_ID, _mix_num))
        # print(sql % (_ID, _mix_ID, _mix_num))
    conn.commit()
    conn.close()


# 展示单菜品信息，和套餐信息
def show():
    conn = sqlite3.connect('./db/menu.db')
    nameTable = ['tbSingle', 'tbMulti']
    tem = {}
    for i in range(2):
        sql = """
       SELECT * FROM %s 
        """
        query = conn.execute(sql % nameTable[i])
        tem[nameTable[i]] = query.fetchall()

    # mul = tem['tbMulti']
    sql_el = '''SELECT
tbMultiElement.Mid,
tbMultiElement.Sid,
tbMultiElement.Snum,
tbSingle.Sname,
tbSingle.Sprice
FROM
tbMultiElement ,
tbSingle
WHERE
tbMultiElement.Sid = tbSingle.Sid
'''
    query_el = conn.execute(sql_el)
    element = query_el.fetchall()
    zucheng = {}
    for i in element:
        if i[0] not in zucheng:
            zucheng[i[0]] = []
        zucheng[i[0]].append(i)

    # print('zucheng', zucheng)

    tem['zucheng'] = zucheng
    conn.close()
    return tem


# 插入用户注册信息
def insert_user(username, password):
    # print('正在db')
    conn = sqlite3.connect('./db/menu.db')
    _username = '"' + username + '"'
    _password = '"' + password + '"'
    sql = """insert into `tbUser` (`Pname`,`Ppsd`)values(%s,%s)"""
    conn.execute(sql % (_username, _password))
    conn.commit()
    conn.close()


# 根据编号得到套餐及单品的详细信息
def query_car(zuhe):
    conn = sqlite3.connect('./db/menu.db')
    tem_m = {}  # 套餐信息
    tem_s = {}  # 单菜品信息
    for item in zuhe:
        # 先根据编号分为套餐和单菜品
        # 分别进行查询，查询后，放入字典
        if item[0] == 'S':
            item_yinhao = '"' + item + '"'
            sql = """SELECT * FROM tbSingle where tbSingle.Sid=%s"""
            query = conn.execute(sql % item_yinhao)
            tem_s[item] = query.fetchall()[0]
        else:
            item_yinhao = '"' + item + '"'
            sql_el = '''SELECT * FROM tbMulti WHERE tbMulti.Mid = %s'''
            query_el = conn.execute(sql_el % item_yinhao)
            tem_m[item] = query_el.fetchall()[0]

    # print('single',tem_s)
    # print('taocan', tem_m)

    conn.close()
    return tem_s, tem_m


# 将点菜单提交到数据库
# tbOrder中插入表单编号，原价，支付价格
# tbDetail：表单编号，菜品编号，数量
def insertCar(li, cost, n_cost, time, user):
    conn = sqlite3.connect('./db/menu.db')

    # 表单编号为算法生成，在原始长度的基础上+1
    sql_length = """select count(*) from `tbOrder` """
    query = conn.execute(sql_length)
    query_lenght = query.fetchone()[0]
    # print('长度', query_lenght)
    id = '"' + 'O' + str(query_lenght).zfill(7) + '"'
    # tbOrder中插入表单编号，原价，支付价格
    sql_order = """insert into `tbOrder` values(%s,%f,%f)"""
    conn.execute(sql_order % (id, cost, n_cost))
    # tbDetail：表单编号，菜品编号，数量
    for item in li:
        ite = '"' + item['id'] + '"'
        num = item['count']
        sql_detail = """insert into `tbDetail` values(%s,%s,%d)"""
        conn.execute(sql_detail % (id, ite, num))
    conn.commit()
    _user =  '"' +user+ '"'
    _time =  '"' +time+ '"'
    sql_time = '''insert into `tbOrderTime` values(%s,%s,%s)'''

    conn.execute(sql_time % (id, _user, _time))
    conn.commit()
    conn.close()
    return 'ok'
