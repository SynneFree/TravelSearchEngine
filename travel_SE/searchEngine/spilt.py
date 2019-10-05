


location1= '中国>北京市>东城区'
location2='中国>四川省>成都市>青羊区'
location3='中国>北京市>东城区>龙潭街道'
location4='中国>四川省>成都市>都江堰市'

location=location4
location=location.replace(' ','').split('>')[1:6]


province = ''+location[0]
if '市' in province:
    province = ''
    city = ''+location[0]
    district =''+ location[1]
else:
    city = ''+location[1]
    district =''+ location[2]

print("省:"+province)
print("市:"+city)
print("区:"+district)

#print(district)