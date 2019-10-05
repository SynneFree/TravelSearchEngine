import xlrd
from elasticsearch import Elasticsearch
import json
es = Elasticsearch()
file="D:/test/data4.xlsx"

def read_excel():
    wb= xlrd.open_workbook(filename=file)
    print(wb.sheet_names())
    sheet1 = wb.sheet_by_index(0)
    rows=sheet1.nrows
    cols=sheet1.ncols
    print("rows:"+str(rows))
    print("cols:" + str(cols))
    count=0
    sum=0
    for c in range(rows):
        count+=1
        if count==1:
            continue
        line=sheet1.row_values(c)
        for i in range(cols):
            line[i]=line[i].replace('&nbsp','&emsp;')
        location=line[10]
        location=location.replace('&emsp;','').replace('&gt;','>').replace(' ','')
        province = ''
        city=''
        district=''
        if location=='':
            pass
        else:
            location2 = location.split('>')[1:6]
            print(location2)
            province = '' + location2[0]
            if '市' in province:
                province = ''
                for i in range(len(location2)):
                    if i==0:
                        city = '' + location2[i]
                    elif i==1:
                        district = '' + location2[i]
            else:
                for i in range(len(location2)):
                    if i==0:
                        province = '' + location2[i]
                    elif i==1:
                        city = '' + location2[i]
                    elif i==2:
                        district = '' + location2[i]
        map = line[18]
        picture=line[19].split(';')[0:3]
        try:
            cover=picture[0]
        except IndexError:
            cover='default_cover.jpg'
        # for i in range(3):
        #     if picture[i]:
        #         pass
        #     else:
        #         picture.append('')
        attention_items=line[13]
        if attention_items=='':
            attention_items="&emsp;&emsp;无"

       # 'related_links': line[17],
        around=line[17].split(';')
        data={
            'name':line[0],
            'location': location,
            'province': province,
            'city': city,
            'district': district,
            'abstract': line[1],
            'distribution': line[2],
            'rank': line[3],
            'feature': line[9],
            'notes': '',
            'strategy': line[4],
            'route': line[14],
            'bestTime': line[15],
            'shopping': line[16],
            'traffic_info': line[5],
            'ticket_info': line[6],
            'openTime': line[7],
            'official_site':line[11],
            'service': line[8],
            'telephone': line[12],
            'attention_items': attention_items,
            'around': around,
            'map':map,
            'picture':picture,
            'cover':cover,
        }
        _in = es.index(index='test_index3', doc_type='basicInfo', body=data)
        print(_in)
        sum+=1
    print("成功插入:"+str(sum))
    # for r in range(2):
    #     for c in range(cols):
    #         ctype=sheet1.cell_type(r,c)
    #         item=sheet1.cell_value(r,c)
    #         if ctype==2 and item%1==0:
    #             item=int(item)
    #         print(item)
    #print(sheet1.row_values(1))
read_excel()