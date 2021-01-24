# flask
# 项目功能 
* 员工管理培训管理系统员工，培训系统需要实现的主要功能包括：
* 公司业总体培训课程的设置和安排。各部门部长课为员工安排相关培训课程 
* 对选课结果进行统计报表。允许员工对培训安排的查询。
* 培训考核成绩的输入和查询。 
* 用户个人信息的修改。 
# 项目目录 
``` 
|—— sql        # 存放相关数据库sql语句
|—— static      # 存放静态资源文件 
|—— |—— css     
|—— |—— images 
|—— |—— js 
|—— templates   # 存放html文件
|—— |—— *.html |—— utils       # 存放一些功能函数，查询以及更新
|—— config.py  #配置文件 
|—— app.py  #启动程序
``` 
# 项目环境
``` 
-安装项目所需要的依赖包，命令如下：
-pip install -r requirements.txt 
``` 
#初始化数据库    
- 在`sql/目录下`命令行进入mysql   
```     
mysql -u root -p    
```     
- 创建数据库   
```     
create database trainplan;  
```     
- 插入数据  
```    
use  trainplan;   
source schema.sql;  
source insert_staff.sql;   
source insert_course.sql;  
source insert_dept.sql;   
source insert_train.sql;  
``` 
#修改配置
``` 
-把config.py的数据库密码改为你自己的数据库密码 
-运行 app.py 
```
也可以参考博客https://blog.csdn.net/qq_53581188/article/details/113092526
