import pymysql
conn=pymysql.connect(host='localhost',user='root',password='',db='data',charset='utf8')
cursor=conn.cursor()
cursor.execute('SELECT * FROM product_info')
print(cursor.fetchall())
cursor.close()
conn.close()