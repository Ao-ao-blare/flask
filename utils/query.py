import pymysql
from config import config

def query(sql):  #数据库查询函数
    # 打开数据库连接
    db = pymysql.connect('123.56.75.35', 'trainplan', config['MYSQL_PASSWORD'], config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()              # 使用 cursor() 方法创建一个游标对象 cursor
    try:
        cur.execute(sql)           # 使用 execute() 方法执行 SQL 查询
        result = cur.fetchall()    #获取查询结果
        db.commit()                #执行sql语句
        return result              #返回查询结果
        #print('query success')
    except:
        # print('query loss')
        db.rollback()              #发生错误时回滚
    cur.close()
    db.close()                     #关闭数据库连接



def update(sql):
    """
    功能; 使用sql语句更新数据库中员工信息。
    参数: sql(string)
    """
    db = pymysql.connect('123.56.75.35', 'trainplan', config['MYSQL_PASSWORD'], config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()           # 使用 execute() 方法执行 SQL 查询
    try:
        cur.execute(sql)
        db.commit()             #执行sql语句
    except:
        db.rollback()           #发生错误时回滚
    cur.close()
    db.close()                  #关闭数据库连接


