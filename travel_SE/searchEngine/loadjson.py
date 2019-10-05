import json

import json
f =open('location.json',encoding='utf-8') #打开‘product.json’的json文件
res=f.read()  #读文件
print(json.loads(res))#把json串变成python的数据类型：字典