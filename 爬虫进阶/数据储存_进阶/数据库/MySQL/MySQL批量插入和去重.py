import pymysql
conn=pymysql.connect(host='localhost',user='root',password='128910',database='spider_data',charset='utf8')
cursor=conn.cursor()
#数据模拟
data = [
    ("华为MateBook D 16", "4299元", "https://detail.zol.com.cn/1"),
    ("联想小新Pro 16", "4999元", "https://detail.zol.com.cn/2"),
    ("苹果MacBook Air", "7999元", "https://detail.zol.com.cn/3"),
    ("苹果MacBook Air", "7999元", "https://detail.zol.com.cn/3")
]
sql = "INSERT IGNORE INTO products (title, price, url) VALUES (%s, %s, %s)"#去重，插入时使用 INSERT IGNORE：如果重复，自动忽略，不报错。
cursor.executemany(sql, data)
conn.commit()
print(f"实际插入 {cursor.rowcount} 条（重复的自动跳过）")

#关闭连接
cursor.close()
conn.close()