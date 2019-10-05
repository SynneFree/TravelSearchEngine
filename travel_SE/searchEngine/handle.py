str = '忻州市（21）\
忻府区（4）\
定襄县（2）\
五台县（3）\
代县（2）\
繁峙县（1）\
宁武县（6）\
静乐县（1）\
偏关县（1）\
原平市（1）\
'


str=str.replace(' ','').replace('（',"',").replace('）',"'").replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','')
str="['"+str+"']"
print(str)