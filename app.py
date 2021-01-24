import json
import math
import re
from flask import Flask, render_template, request, flash, jsonify, redirect, url_for, session, g
from sqlalchemy.sql.functions import user
from werkzeug.datastructures import ImmutableMultiDict
from utils import query
import config
from  flask_paginate import Pagination,get_page_parameter
# 创建flask对象
app = Flask(__name__)
app.config['SECRET_KEY'] = 'gsolvit'

#登录界面，默认访问界面
@app.route('/', methods=['GET', 'POST'])  # 首先打开的界面
@app.route('/Login.html', methods=['GET', 'POST'])  # 首先打开的界面
@app.route('/login', methods=['GET', 'POST'])  # 获取路由，进入登录界面
def login():
    if request.method == 'GET':
        return render_template('Login.html')
    else:
        sta_id = request.form.get('sta_id')             #获取表单提交的账号
        password = request.form.get('password')         #获取表单提交的密码
        sql = "select * from trainplan.staff where STA_NO = '%s'" % sta_id
        result = query.query(sql)
        if result:
            if result[0][10] == password:  # 判断密码是否相同，result[][密码在数据库中的列数-1]
                session['sta_id'] = result[0][2]
                session['user'] = result[0][0]
                session['job'] = result[0][5]
                session.permanent = True  # permanent是“永久”的意思，如果设置了此项为True，意味着在permanent_session_lifetime过期时间内即使关闭浏览器，再次打开时session还有效
                if session['job'] == '部长':
                    return redirect(url_for('index'))       #重定向到index函数
                else:
                    return redirect(url_for('staff_index'))  #重定向到staff-index函数
            else:
                return u'账号或密码错误'
        else:
            return u'不存在这个用户'


##管理员所见部门界面
@app.route('/AdmitDept.html', methods=['GET', 'POST'])
def AdmitDept():
    user = session['user']          #获取当前网站登录的用户
    sql = "select * from dept"
    result = query.query(sql)
    sql = "select COUNT(NAME) number FROM dept"
    staff = query.query(sql)
    staff = staff[0]                #返回的结果类型为元组，当返回的元组中只有一个元素时，要取两次才可以把里面的值取出来
    total = staff[0]
    return render_template('AdmitDept.html',result = result,user=user,total = total)


# 管理员所见界面
#管理员所见员工界面
@app.route('/StaffInfo.html', methods=['GET', 'POST'])
def staffinfo():
    curpage = request.args.get('page')        #获取用户当前所在的页面数
    if curpage is None:                       # 如果没有page则显示第一页
        curpage = 1
        start = 0                             #设置每页显示多少条数据
        end = 10
    else:
        start = (int(curpage) - 1) * 10
        end = int(curpage) * 10
    user = session.get('user')
    sql = "select * from trainplan.staff"
    result = query.query(sql)
    sql = "select COUNT(NAME) number FROM staff"
    staff = query.query(sql)
    staff = staff[0]
    if type(staff[0]/10) == float:      #计算总页数，如果有余数，则总页数为商加一
        page = int(staff[0]/10 + 1)
    else:
        page = int(staff[0]/10)
    return render_template('StaffInfo.html',user=user,total = staff[0],page = page,result = result[start:end])

#管理员所见课程界面
@app.route('/AdmitCourse.html', methods=['GET', 'POST'])
def AdmitCourse():
    user = session.get('user')
    sql = "select * from course"
    result = query.query(sql)
    sql = "select COUNT(NAME) number FROM course"
    staff = query.query(sql)
    staff = staff[0]
    total = staff[0]
    return render_template('AdmitCourse.html',result = result,user=user,total = total)

#管理员所见员工培训界面
@app.route('/StaffTrain.html', methods=['GET', 'POST'])
def StaffTrain():
    curpage = request.args.get('page')      #获取用户当前所在的页面数
    if curpage is None:                     # 如果没有page则显示第一页
        curpage = 1
        start = 0                           #设置每页显示多少条数据
        end = 10
    else:
        start = (int(curpage) - 1) * 10
        end = int(curpage) * 10
    user = session.get('user')
    sql = "select * from train"
    result = query.query(sql)
    sql = "select COUNT(NAME) number FROM train"
    staff = query.query(sql)
    staff = staff[0]
    if type(staff[0] / 10) == float:            #计算总页数，如果有余数，则总页数为商加一
        page = int(staff[0] / 10 + 1)
    else:
        page = int(staff[0] / 10)
    return render_template('StaffTrain.html',user=user,total = staff[0],page = page,result = result[start:end])


#管理员所见首页
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    sta_id = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % sta_id
    result = query.query(sql)
    sql = "select COUNT(NAME) number FROM staff"
    staff = query.query(sql)
    staff = staff[0]
    sql = "SELECT COUNT(ID) as total FROM dept"
    dept = query.query(sql)  # 总记录//dept返回的是元组。（（5，））是个套娃怪
    dept = dept[0]  # 总页数
    sql = "select COUNT(NAME) number FROM course"
    course = query.query(sql)
    course = course[0]
    #计算各个部门的员工数
    sql = "select COUNT(NAME) number FROM staff where DEPT = '公开挑逗客户部' "
    dept1 = query.query(sql)
    dept1 = dept1[0]
    sql = "select COUNT(NAME) number FROM staff where DEPT = '遇事诈尸部' "
    dept2 = query.query(sql)
    dept2 = dept2[0]
    sql = "select COUNT(NAME) number FROM staff where DEPT = '一天到晚尽没事部' "
    dept3 = query.query(sql)
    dept3 = dept3[0]
    sql = "select COUNT(NAME) number FROM staff where DEPT = '游山玩水部' "
    dept4 = query.query(sql)
    dept4 = dept4[0]
    sql = "select COUNT(NAME) number FROM staff where DEPT = '葬爱家族续命部' "
    dept5 = query.query(sql)
    dept5 = dept5[0]
    #计算各个课程的选择数
    sql = "select COUNT(NAME) number FROM train where COURSE = '僵尸逃生课' "
    COURSE1 = query.query(sql)
    COURSE1 = COURSE1[0]
    sql = "select COUNT(NAME) number FROM train where COURSE = '名侦探柯南与化学探秘' "
    COURSE2 = query.query(sql)
    COURSE2 = COURSE2[0]
    sql = "select COUNT(NAME) number FROM train where COURSE = '哈利波特与遗传学' "
    COURSE3 = query.query(sql)
    COURSE3 = COURSE3[0]
    sql = "select COUNT(NAME) number FROM train where COURSE = '性感高跟鞋研究' "
    COURSE4 = query.query(sql)
    COURSE4 = COURSE4[0]
    sql = "select COUNT(NAME) number FROM train where COURSE = '水中编篮' "
    COURSE5 = query.query(sql)
    COURSE5 = COURSE5[0]
    sql = "select COUNT(NAME) number FROM train where COURSE = '浪费时间有理课' "
    COURSE6 = query.query(sql)
    COURSE6 = COURSE6[0]
    return render_template('index.html',result = result,staff=staff[0], dept = dept[0], course = course[0],
                           dept1 = dept1[0],dept2=dept2[0],dept3 = dept3[0],dept4 = dept4[0],dept5 = dept5[0],
                           COURSE1=COURSE1[0],COURSE2 = COURSE1[0],COURSE3 = COURSE1[0],COURSE4 = COURSE1[0],
                           COURSE5 = COURSE1[0],COURSE6 = COURSE1[0],)


#普通员工所见首页
@app.route('/staff_index.html', methods=['GET', 'POST'])
def staff_index():
    sta_id = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % sta_id
    result = query.query(sql)
    sql = "select * from course "
    course = query.query(sql)
    sql = "select * from train "
    train = query.query(sql)
    return render_template('staff_index.html',result = result,train = train[4], course = course)

#普通员工我的课程
@app.route('/staff_train.html', methods=['GET', 'POST'])
def staff_train():
    sta_id = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % sta_id
    result = query.query(sql)
    sql = "select * from train WHERE STA_ID='%s'" % result[0][2]
    train = query.query(sql)
    sql = "select * from course WHERE NAME='%s'" % train[0][2]
    course = query.query(sql)
    return render_template('staff_train.html',result = result,train = train,course=course[0])

#小图标的编辑与删除
#员工小图标编辑，表单接收
@app.route('/edit_staff', methods=['GET', 'POST'])
def edit_staff():
    sql = "UPDATE trainplan.staff SET DEPT='%s',JOB='%s' WHERE STA_NO='%s'" % (request.values['dept'],request.values['job'],request.values['id'])
    query.update(sql)

#员工小图标删除
@app.route('/del_staff', methods=['GET', 'POST'])
def del_staff():
    sql = "DELETE FROM trainplan.staff WHERE STA_NO = '%s'" % request.values['id']
    query.query(sql)

#部门小图标修改
@app.route('/edit_dept', methods=['GET', 'POST'])
def edit_dept():
    sql = "UPDATE trainplan.dept SET ID='%s',NAME='%s',ADMIN='%s',INTRO='%s' WHERE ID='%s'" % (
    request.values['ID'], request.values['NAME'], request.values['ADMIN'], request.values['INTRO'], request.values['id'])
    query.update(sql)

#课程小图标删除
@app.route('/del_course', methods=['GET', 'POST'])
def del_course():
    sql = "DELETE FROM trainplan.staff WHERE STA_NO = '%s'" % request.values['id']
    query.query(sql)

#课程小图标修改
@app.route('/edit_course', methods=['GET', 'POST'])
def edit_course():
    sql = "UPDATE trainplan.course SET NO='%s',NAME='%s',TEACHER='%s',INTRO='%s',BOOK='%s'," \
          "START_TIME='%s',END_TIME='%s',CLASS_TIME='%s',MAX_STAFFS='%s'," \
          "CLASS_ADDRESS='%s',STATE='%s' WHERE NO='%s'" % (
    request.values['NO'], request.values['NAME'],request.values['TEACHER'], request.values['INTRO'],request.values['BOOK'],
    request.values['START_TIME'],request.values['END_TIME'], request.values['CLASS_TIME'],request.values['MAX_STAFFS'],
    request.values['CLASS_ADDRESS'],request.values['STATE'], request.values['id'])
    query.update(sql)

#培训小图标修改
@app.route('/edit_train', methods=['GET', 'POST'])
def edit_train():
    sql = "UPDATE trainplan.train SET NAME='%s',STA_ID='%s',COURSE='%s',SCORE='%s',CHECK_TIME='%s',EVALUATE='%s'  WHERE NAME='%s'" % (
    request.values['NAME'], request.values['STA_ID'],request.values['COURSE'], request.values['SCORE'],request.values['CHECK_TIME'],request.values['EVALUATE'], request.values['id'])
    query.update(sql)


#用户个人界面
#员工个人信息界面
@app.route('/Person.html', methods=['GET', 'POST'])
def person():
    sta_id = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % sta_id
    result = query.query(sql)
    return render_template('Person.html',result = result)

#修改密码
@app.route('/edit_pwd.html', methods=['GET', 'POST'])
def edit_pwd():
    sta_id = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % sta_id
    result = query.query(sql)
    return render_template('edit_pwd.html',result = result)

#修改密码，表单接收
@app.route('/PWDedit', methods=['GET', 'POST'])
def PWDedit():
    sta_id = session.get('sta_id')
    oldpwd = request.form.get('oldpwd')
    sql = "select * from trainplan.staff where STA_NO = '%s'" % sta_id
    result = query.query(sql)
    if len(result) != 0:
        # print(result[0][10], password)#查询数据库中密码是否与输入的相同，result[][密码在数据库中的列数-1]
        if result[0][10] == oldpwd:  # 判断密码是否相同
            newpwd = request.form.get('newpwd')
            confirmpwd = request.form.get('confirmpwd')
            if(newpwd != confirmpwd):
                return u'两次输入的密码不一致'
            else:
                sql = "UPDATE trainplan.staff SET PASSWORD='%s' WHERE STA_NO='%s'" % (confirmpwd,  sta_id)
                query.update(sql)
                return render_template('edit_pwd.html',result = result)
        else:
            return u'密码错误'

#个人编辑界面，表单接收
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    sta_id = session.get('sta_id')
    name = request.form.get('name')
    sex = request.form.get('sex')
    birth = request.form.get('birth')
    edu = request.form.get('edu')
    address = request.form.get('address')
    tel = request.form.get('tel')
    intro = request.form.get('intro')
    sql = "UPDATE trainplan.staff SET NAME='%s',SEX='%s',BIRTH='%s',EDU='%s' ,ADDRESS='%s',TEL='%s',introduction='%s' WHERE STA_NO='%s'" % (
        name, sex, birth,  edu, address, tel, intro,sta_id)
    query.update(sql)
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % sta_id
    result = query.query(sql)
    return render_template('Person.html',result = result)

#添加信息
#添加部门
@app.route('/dept_add.html', methods=['GET', 'POST'])
def dept_add():
    sta_id = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % sta_id
    result = query.query(sql)
    return render_template('dept_add.html',result = result)

#添加员工
@app.route('/staff_add.html', methods=['GET', 'POST'])
def staff_add():
    sta_id = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % sta_id
    result = query.query(sql)
    return render_template('staff_add.html',result = result)

#添加课程
@app.route('/course_add.html', methods=['GET', 'POST'])
def add_C():
    sta_id = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % sta_id
    result = query.query(sql)
    return render_template('course_add.html',result = result)

#添加部门，表单接收
@app.route('/addDept', methods=['GET', 'POST'])
def addDEPT():
    user = session.get('sta_id')
    id = request.form.get('id')
    name = request.form.get('name')
    admit = request.form.get('admit')
    intro = request.form.get('intro')
    sql = "INSERT INTO trainplan.dept (ID,NAME,ADMIN,INTRO)VALUES ('%s','%s','%s','%s')" % (id,name,admit,intro)
    query.update(sql)
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % user
    result = query.query(sql)
    return render_template('AdmitDept.html',result = result)

#添加课程，表单接收
@app.route('/addCourse', methods=['GET', 'POST'])
def addCourse():
    user = session.get('sta_id')
    id = request.form.get('id')
    name = request.form.get('name')
    teacher = request.form.get('teacher')
    intro = request.form.get('intro')
    book= request.form.get('book')
    start = request.form.get('start')
    end = request.form.get('end')
    time = request.form.get('time')
    max= request.form.get('max')
    address = request.form.get('address')
    status = request.form.get('status')
    sql = "INSERT INTO trainplan.course (NO,NAME,TEACHER,INTRO,BOOK,START_TIME,END_TIME,CLASS_TIME,MAX_STAFFS,CLASS_ADDRESS,STATE)" \
          "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (id,name,teacher,intro,book,start,end,time,max,address,status)
    query.update(sql)
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % user
    result = query.query(sql)
    return render_template('AdmitCourse.html',result = result)

#添加员工，表单接收
@app.route('/addStaff', methods=['GET', 'POST'])
def addStaff():
    user = session.get('sta_id')
    name = request.form.get('name')
    sex = request.form.get('sex')
    sta_no = request.form.get('id')
    birth = request.form.get('birth')
    dept = request.form.get('dept')
    job = request.form.get('job')
    edu = request.form.get('edu')
    address = request.form.get('address')
    tel = request.form.get('tel')
    introduction = request.form.get('intro')
    pwd = request.form.get('pwd')
    sql = "INSERT INTO trainplan.staff (NAME,SEX,STA_NO,BIRTH,JOB,EDU,ADDRESS,TEL,introduction,PASSWORD)" \
          "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
          name, sex, sta_no, birth, dept, job, edu, address, tel, introduction, pwd)
    query.update(sql)
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % user
    result = query.query(sql)
    return render_template('StaffInfo.html', result=result)

#搜索返回界面
#搜索员工，管理员
@app.route('/selStaff', methods=['GET', 'POST'])
def selStaff():
    user = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % user
    result = query.query(sql)
    text = request.values.get('keyword')
    sel = request.values.get('search_field')#获取文本＆单选框
    sql = "select * from trainplan.staff WHERE STA_NO='%s' or NAME='%s' or DEPT = '%s'" % (text,text,text)
    RS = query.query(sql)
    #total = RS[0]
    if RS:
        return render_template('SELStaff.html', result=result,RS = RS,user = user)
    else:
        return u'不存在这个用户'

#搜索部门，管理员
@app.route('/SELdept', methods=['GET', 'POST'])
def selDept():
    user = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % user
    result = query.query(sql)
    text = request.values.get('keyword')
    sel = request.values.get('search_field')#获取文本＆单选框
    sql = "select * from trainplan.dept WHERE ID='%s' or NAME='%s' or ADMIN = '%s'" % (text,text,text)
    RS = query.query(sql)
    #total = RS[0]
    if RS:
        return render_template('SELdept.html', result=result,RS = RS,user = user)
    else:
        return u'不存在这个用户'

#搜索课程，管理员
@app.route('/SELcourse', methods=['GET', 'POST'])
def selCourse():
    user = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % user
    result = query.query(sql)
    text = request.values.get('keyword')
    sel = request.values.get('search_field')#获取文本＆单选框
    sql = "select * from trainplan.course WHERE NO='%s' or NAME='%s' or TEACHER = '%s'" % (text,text,text)
    RS = query.query(sql)
    #total = RS[0]
    if RS:
        return render_template('SELcourse.html', result=result,RS = RS,user = user)
    else:
        return u'不存在这个用户'

#搜索培训，管理员
@app.route('/SELtrain', methods=['GET', 'POST'])
def selTrain():
    user = session.get('sta_id')
    sql = "select * from trainplan.staff WHERE STA_NO='%s'" % user
    result = query.query(sql)
    text = request.values.get('keyword')
    sel = request.values.get('search_field')#获取文本＆单选框
    sql = "select * from trainplan.train WHERE NAME='%s' or STA_ID='%s' or SCORE = '%s'" % (text,text,text)
    RS = query.query(sql)
    #total = RS[0]
    if RS:
        return render_template('SELcourse.html', result=result,RS = RS,user = user)
    else:
        return u'不存在这个用户'

if __name__ == '__main__':
    app.run("127.0.0.0 :5000", debug=True)
