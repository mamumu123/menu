from flask import Flask, render_template, request, url_for, jsonify, json, redirect, session
from flask_bootstrap import Bootstrap
import db  # 导入数据库相关操作
import cal  # 导入线性规划算法

app = Flask(__name__)
app.secret_key = '\xf1\x92Y\xdf\x8ejY\x04\x96\xb4V\x88\xfb\xfc\xb5\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'
Bootstrap(app)


# 主页
@app.route('/', methods=['POST', 'GET'])
def index():
    # 判断是否已经登陆，如果还没有登陆，退回到登录界面
    username = session.get('username')
    # 如果还没有登录，就返回登录页面
    if username == None:
        return redirect(url_for('login'))
    # 从数据库中获取展示数据
    data = db.show()
    return render_template('index.html', all_message=data, user=username)


# 登陆
@app.route("/login", methods=["POST", "GET"])
def login():
    # 如果提交，开始处理
    if request.method == 'POST':
        # 提交，即开始验证
        # 得到用户名，密码
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        username = session['username']
        password = session['password']
        # 表单提交，检查数据库中有无此用户，以及密码是否正确
        result = db.check_user(username, password)
        # 此用户名不存在
        if result is None:
            return render_template('login.html', errorMessage='此用户名不存在')
        # 密码错误
        if result[3] != password:
            return render_template('login.html', errorMessage='密码错误')
        # 如果类型为1，即为管理员，重定向到管理员界面
        if result[2] == 1:
            return redirect('admin')
        # 如果类型为0，即为普通用户，重定向到主页
        if result[2] == 0:
            return redirect(url_for('index'))
    # 如果不是提交表单，即打开登录页面
    return render_template('login.html')


# 登出
@app.route("/logout")
def logout():
    # 登出，清除session，返回登录界面
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))


# 注册
@app.route("/register", methods=["POST", "GET"])
def register():
    # 如果是表单提交
    if request.method == 'POST':
        # print('正在注册')
        # 提交，即开始验证
        username = request.form['username']
        password = request.form['password']
        # 注册
        db.insert_user(username, password)
        # 如果注册成功，返回登录界面，重新登录，即可进入主界面
        return redirect(url_for('login'))
    return render_template('register.html')


# 管理页面
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    # 检查是否已经登录
    username = session.get('username')
    # 如果还没有登陆，则返回登陆界面
    if username == None:
        return redirect(url_for('login'))
    # 得到展示数据
    message = db.show()
    # print('tbSingle', message['tbSingle'])
    return render_template('admin.html', single=message['tbSingle'])


# 增加单品
@app.route('/admin/insertMenu', methods=['POST', 'GET'])
def admin_insertMenu():
    # 得到前台提交的数据
    data = request.get_json()
    dataForm = data.get('dataForm')
    # print(dataForm)
    # 插入单品
    db.insertMenu(dataForm)
    return 'OK'


# 增加套餐
@app.route('/admin/insertMul', methods=['POST', 'GET'])
def admin_insertMul():
    # 得到前台提交的数据
    data = request.get_json()
    dataForm = data.get('dataForm')
    # 插入套餐
    db.insertMul(dataForm)
    return 'OK'


# 将单品组合套餐，线性规划
@app.route('/index/cal_sum', methods=['POST', 'GET'])
def cal_sum():
    # 得到前台提交的数据
    data = request.get_json()
    li = data.get('list')
    cal_da = {}
    # 将数据整理为 dict{id:数量}
    for per in li:
        cal_da[per['id']] = per['count']
    # 函数cal：线性规划，计算
    # cost：最低价格
    # zuhe：最低价格的套餐搭配
    cost, zuhe = cal.cal(cal_da)
    # 函数：add_cal：计算添加一个菜品，能节省的花费最多，
    # target_single：计算得到将要添加的菜品
    # target_min：节省的花费
    # target_dict：套餐搭配
    target_single, target_min, target_dict = cal.add_cal(cal_da)
    # query_car：根据编号得到套餐及单品的详细信息
    # tem_s：单品详细信息
    # tem_m ：套餐详细信息
    tem_s, tem_m = db.query_car(zuhe)
    # 根据编号得到套餐及单品的详细信息
    # target_s：单品详细信息
    # target_m 套餐详细信息
    target_s, target_m = db.query_car(target_dict)
    # 合成将要返回的数据
    result = {
        'cost': cost,
        'tem_s': tem_s,
        'tem_m': tem_m,
        'num': zuhe,
        'target_single': target_single,
        'target_min': target_min,
        'target_s': target_s,
        'target_m': target_m,
        'target_num': target_dict
    }
    # 将得到的数据返回前端
    return json.dumps(result)


# 支付，提交表单到数据库
@app.route('/index/sub_mit', methods=['POST', 'GET'])
def sub_mit():
    # 得到前端的数据
    data = request.get_json()
    li = data.get('list')
    cost = data.get('cost')
    n_cost = data.get('new_cost')
    time = data.get('time')
    user = data.get('user')
    # 提交支付信息，插入数据库
    print('time', time)
    print('user', user)
    db.insertCar(li, cost, n_cost, time, user)
    return 'OK'


# 404页面
@app.errorhandler(404)
def page_not_find(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
