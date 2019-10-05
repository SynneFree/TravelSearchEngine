import xlrd
from elasticsearch import Elasticsearch
es = Elasticsearch()
file="D:/test/99data.xlsx"
import json




str1='&nbsp&nbsp 中国&gt;黑龙江省&gt;七台河市&gt;桃山区 '
str2='&nbsp&nbsp三亚大东海，"水暖沙白滩平"，是海南最著名的海滩之一、冬泳避寒胜地，也是三亚开发较早、较成熟的 海滨度假区。' \
     '大东海海湾与榆林港毗邻，在兔尾岭和鹿回头两个山头中间，湾形宛如月牙，海面辽阔平静，海水晶莹碧蓝，形成一幅白沙、阳光、碧水、沙滩、绿树组成的美丽热带风光图画，' \
     '这也使大东海斐声海内外。  <br>&nbsp&nbsp大东海三面环山，一面大海，一排排翠绿椰林环抱沙滩，五颜六色的海滩贝壳散布在海滩上，' \
     '信手可得。辽阔的海面晶莹如镜，叠印着蓝天、白云、岱山的倒影；远处水天一色，似有若无的浪花，三三两两的渔船，风景美如画。' \
     '伫立在大东海之滨，眺望着宁静而辽阔的海景，可感到才思阔朗、神清气爽，甚至还会有浑身有扭转乾坤之气概，无论春夏秋冬，' \
     '这里都是中国南方地区最理想的海滨天然游泳场，也是一个不可多得的滨海度假游览区。 '

str3='8c3aef849c8789a46c220ab0699a.jpg;9035b17d2e3c4e031571521cda61.jpg;'

print(str1)
res1=str1.count('&nbsp',0,len(str1))
str1=str1.replace('&gt;','>').replace('&nbsp','').replace(' ','')
print(str1)
print(res1)

img=[]

img=str3.split(';')[0:3]
print(img)

img=json.dumps(img)

print(img)