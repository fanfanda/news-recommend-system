import pandas as pd
import numpy as np
import sys
term_dict={}

data = pd.read_csv('/Users/steven/Documents/add_title.csv',encoding='GB18030')
data['jieba_10']=data.jieba_10.apply(lambda x:eval(x))


print('delete dumplicates.....')
dele_dumplicates=data[['news_id','jieba_10','content','title']]
dele_dumplicates=dele_dumplicates.drop_duplicates(subset=['news_id']).reset_index(drop=True)
for i in range(len(dele_dumplicates)):
    if type(dele_dumplicates.loc[i,'content'])==float:
        dele_dumplicates.loc[i,'content']=''

term_vec=[]
for i in range(len(dele_dumplicates)):
    for j in data.loc[i,'jieba_10']:
        if j in term_dict.keys():
           term_dict[j]+=1
        else:
           term_dict[j]=1
           term_vec.append(j)

        
print(len(term_dict))
word2vec=[]
term_vec_dict={}
print('create matrix....')
for i in range(len(dele_dumplicates)):
    temp_vec=[]
    if i%1000==0:
        print(i)
    for j in term_dict.keys():
        if j in dele_dumplicates.loc[i,'jieba_10']:
            temp_vec.append(str(dele_dumplicates.loc[i,'content']+dele_dumplicates.loc[i,'title']).count(j))
        else:
            temp_vec.append(0)
    word2vec.append(temp_vec)
print('write file....')
file=open('data.txt','w')
file.write(str(word2vec))
file.close()
def f_process_matric_U(matric_U,Save_N_Singular_value):
    """according to the matric U, choose the words as the feature in each document,根据前N个奇异值对U进行切分,选择前N列""" 
    document_matric_U=[]
    for line in matric_U:
        line_new=line[:Save_N_Singular_value]
        document_matric_U.append(line_new)
    return document_matric_U

def f_process_matric_S(matric_S,Save_information_value):
    """choose the items with large singular value,根据保留信息需求选择奇异值个数"""
    matricS_new=[]
    S_self=0
    N_count=0
    Threshold=sum(matric_S)*float(Save_information_value)
    for value in matric_S:
        if S_self<=Threshold:
            matricS_new.append(value)
            S_self+=value
            N_count+=1
        else:
            break
    print ("the %d largest singular values keep the %s information " %(N_count,Save_information_value))
    return (N_count,matricS_new)

def f_process_matric_V(matric_V,Save_N_Singular_value):
    """according to the matric V, choose the words as the feature in each document,根据前N个奇异值对U进行切分,选择前N行"""
    document_matric_V=matric_V[:Save_N_Singular_value]
    return document_matric_V
def f_combine_U_S_V(matric_u,matric_s,matirc_v):
    """calculate the new document对奇异值筛选后重新计算文档矩阵"""
    
    new_document_matric=np.dot(np.dot(matric_u,np.diag(matric_s)),matirc_v)
    return new_document_matric

def f_matric_to_document(document_matric,word_list_self):
    """transform the matric to document,将矩阵转换为文档"""
    new_document=[]
    for line in document_matric:
        count=0
        for word in line:
            if float(word)>=0.5:                                                                                     #转换后文档中词选择的阈值
                new_document.append(word_list_self[count]+" ")
            else:
                pass
            count+=1
        new_document.append("\n")
    return new_document
print('load_data......')
file=open('data.txt','r')
aa=file.read()
a=eval(aa)
print('svd....')
U,S,V=np.linalg.svd(a)
print('rebuild matrix....')
N_count,document_matric_S=f_process_matric_S(S,0.5)
document_matric_U=f_process_matric_U(U,N_count)
document_matric_V=f_process_matric_V(V,N_count)
new_document_matric=f_combine_U_S_V(document_matric_U,document_matric_S,document_matric_V)
dele_dumplicates['svd_topic_5']=''
print('update topic')
tempp_dic={}
for i in range(len(dele_dumplicates)):
    temp_index=new_document_matric[i].argsort()[-5:]
##    print(temp_index)
    temp_topic_vec=[]
    for j in reversed(temp_index):
        temp_topic_vec.append(term_vec[j])
    dele_dumplicates[i,'svd_topic_5']=str(temp_topic_vec)
    tempp_dic[dele_dumplicates.loc[i,'news_id']]=temp_topic_vec
data['topic_5']=''
print('write_data.....')

for i in range(len(data)):
    data.loc[i,'topic_5']=str(tempp_dic[data.loc[i,'news_id']])
data.to_csv('after_svd_0_5.csv',encoding='GB18030')


##for i in range(len(new_document_matric)):
    
##print(sorted(new_document_matric[1],reverse=True))
##print(U,S,V)


