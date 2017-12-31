import pandas as pd
import numpy as np
import datetime
import copy
import sys
term_dict={}

data = pd.read_csv('/Users/steven/Documents/after_svd_0_5.csv',encoding='GB18030')
data['jieba_10']=data.jieba_10.apply(lambda x:eval(x))
data['topic_5']=data.topic_5.apply(lambda x:eval(x))

hou10_term_vec=[]
user_dict={}
test_user_dict={}
count=0
print('generate dict......')
for i in range(len(data)):
    if int(data.loc[i,'browse_time'])>int(1395331200):
        for j in data.loc[i,'topic_5']:
           hou10_term_vec.append(j)
        test_user_dict[data.loc[i,'user_id']]={}
    else:
        count+=1
        if data.loc[i,'user_id'] in user_dict.keys():
            for j in data.loc[i,'topic_5']:
                 user_dict[data.loc[i,'user_id']].append(j)
        else:
            user_dict[data.loc[i,'user_id']]=copy.deepcopy(data.loc[i,'topic_5'])
hou10_term_vec=list(set(hou10_term_vec))
print('update user_dict......')
for i in test_user_dict.keys():
    if i in user_dict.keys():
        test_user_dict[i] = list(set(user_dict[i]).intersection(set(hou10_term_vec)))
print('-------evaluate------')
correct=0
not_in=0
sum_in=0
for i in range(len(data)):
    if int(data.loc[i,'browse_time'])>int(1395331200):
        sum_in+=1
        if data.loc[i,'user_id'] in user_dict.keys():
            if len(list(set(user_dict[data.loc[i,'user_id']]).intersection(set(data.loc[i,'topic_5']))))!=0:
                correct+=1
        else:
            not_in+=1
print(correct,not_in,sum_in,correct/(sum_in-not_in))
    
##for i in test_user_dict.keys():
##    if len(test_user_dict[i])!=0:
##        print(i,test_user_dict[i])
##        break

##for i in range(len(data)):
##    #about not cold start
##    if int(data.loc[i,'browse_time'])<=int(1395331200) and data.loc[i,'user_id'] in user_dict.keys():
##        user_dict[]

            
            
        
   
        


        
