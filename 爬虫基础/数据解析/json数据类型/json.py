import json
books = [
    {
        "title": "《蛊真人》",
        "author": "蛊真人",
        "year": 2015,
        "tags": ["玄幻", "重生", "魔道"],
        "price": 29.9,
        "in_stock": True
    },
    {
        "title": "《三体》",
        "author": "刘慈欣",
        "year": 2008,
        "tags": ["科幻", "史诗"],
        "price": 49.9,
        "in_stock": False
    },
    {
        "title": "《活着》",
        "author": "余华",
        "year": 1993,
        "tags": ["小说", "现实主义"],
        "price": 35.0,
        "in_stock": True
    }
]
json_str_pretty = json.dumps(books, indent=2, ensure_ascii=False)#现在数据变成了，json
#indent：缩进空格数，使 JSON 更可读。
# ensure_ascii=False：允许输出原始中文（默认会将中文转义为 \u...）
json_str_pretty= json.loads(json_str_pretty) #现在就变成了python数据类型
print(json_str_pretty)
print(type(json_str_pretty))
print(json_str_pretty[0])
print(type(json_str_pretty[0]))
print(json_str_pretty[0]['title'])#输出蛊真人