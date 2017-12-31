import pandas as pd
import datetime
import numpy as np
import jieba
import jieba.analyse
import sys
user_dict={}

data = pd.read_table('/Users/steven/Documents/课程学习资料/网络数据挖掘/大作业/新闻推荐/user_click_data.txt',header=None,delim_whitespace=True)
data.columns = ['user_id', 'news_id', 'browse_time', 'title', 'content', 'time']

data['change_browse_time']=data.browse_time.apply(lambda x:datetime.datetime.fromtimestamp(int(x)))
##for i in range(len(data)):
##    if data.loc[i,'change_browse_time']<=datetime.datetime.fromtimestamp(1395331200):
##        user_dict[data.loc[i,'user_id']]=1
##print(len(user_dict))

#filter content==nan
##data=data[pd.notnull(data['content'])].reset_index(drop=True)

for i in range(len(data)):
    if type(data.loc[i,'content'])==float:
        data.loc[i,'content']=''
data['jieba_10']=''


for i in range(len(data)):
    temp=jieba.analyse.extract_tags(data.loc[i,'content']+data.loc[i,'title'],10)
    data.loc[i,'jieba_10']=str(temp)
data.to_csv('add_title.csv',encoding='GB18030')
##f = open('ffd.txt','wb')
##f.write(vector)
##f.close()
