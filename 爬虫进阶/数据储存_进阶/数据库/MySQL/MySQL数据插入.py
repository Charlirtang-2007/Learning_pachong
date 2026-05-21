import pymysql
conn=pymysql.connect(host='localhost',user='root',password='',db='spider_data',charset='utf8')
cursor=conn.cursor()#游标（用于执行 SQL 语句）
# 创建数据库（如果不存在）
cursor.execute("CREATE DATABASE IF NOT EXISTS spider_data")
cursor.execute("USE spider_data")#使用spider_data数据库
#创建表的 SQL
create_table_sql ="""
    CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,   
    title VARCHAR(255) NOT NULL,         
    price VARCHAR(50),                   
    url VARCHAR(500) UNIQUE,             
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
cursor.execute(create_table_sql) #执行步骤
# 爬虫获取的数据（模拟）
id=1
title = "华为MateBook D 16"
price = "4299元"
url = "https://detail.zol.com.cn/xxx"
# 插入数据
insert_sql = "INSERT INTO products (id,title, price, url) VALUES (%s, %s, %s,%s)"#（使用占位符 %s，防止 SQL 注入）
cursor.execute(insert_sql, (id,title, price, url)) # 4. 执行插入
# 提交事务（非常重要！）不提交数据不会真正写入数据库
conn.commit()

#关闭连接
cursor.close()
conn.close()