import pandas as pd
import numpy as np
import ast
import json
import copy

# read files
train_messages=pd.read_csv('user_messages.csv')
test_messages=pd.read_csv('user_messages_test.csv')
user_data=pd.read_csv('user_data.csv',
                      usecols=['event_time','user_id','event','ad_id'])

ad_category_df=pd.read_csv('ads_data.csv', usecols=['ad_id','enabled','category_id'])
ad_category_en=ad_category_df.set_index('ad_id').to_dict()
print 'done reading'

# convert formats
user_data.event_time=pd.to_datetime(user_data.event_time)
train_messages.ads=train_messages.ads.apply(ast.literal_eval)

#build category dic
c_dic={}
def dic_build(row):
    global c_dic
    if row.category_id not in c_dic:
        c_dic[row.category_id]=row.ads
    else:
        c_dic[row.category_id].extend(row.ads)
train_messages.apply(dic_build, axis=1)

#  sort user data 
user_data.sort_values('event_time',inplace=True)

# different df for message
user_data_ms=user_data[user_data.event=='first_message']

#build user dictionaries
user_dic2={}
for user_ob in user_data[user_data.event=='view'].groupby('user_id'):
    df=user_ob[1]
    ads=list(df.ad_id)
    user_dic2[user_ob[0]]=ads

user_dic3={}
for user_ob in user_data_ms.groupby('user_id'):
    df=user_ob[1]
    ads=list(df.ad_id)
    user_dic3[user_ob[0]]=ads

# function to be executed for each user-category pair
def find_sim(row):
    user_id=row['user_id']
    cat_id=row['category_id']

    # handle case of cold start
    if user_id not in user_dic2:
        s=pd.Series(list(c_dic[cat_id]))
        p= list(s.value_counts().index)
        temp=[]
        for i,ad in enumerate(p):
            temp.append(ad)
        return temp[:10]

    # find all ads of the given category for that user 
    ads=user_dic2[(user_id)]
    temp=[]
    for ad in ads:
        if ad_category_en['category_id'][ad]==cat_id:
            if ad_category_en['enabled'][ad]==1:
                    temp.append(ad)

    # descending order
    temp.reverse()

    # find recent ads
    recent=temp[:100]

    # find popular ads
    popular=pd.Series(temp).value_counts().index
    pop_c=list(pd.Series(temp).value_counts())

    # initialize prediction list
    pred=[]

    # append popular
    for i,elem in enumerate(popular):
        if elem not in pred:
            if pop_c[i]>1:
                pred.append(elem)

    # append recent
    for elem in recent:
        if elem not in pred:
            pred.append(elem)

    # append trending
    s=pd.Series(list(c_dic[cat_id]))
    p= list(s.value_counts().index)
    for i,adaa in enumerate(p):
            if adaa not in pred:
                    pred.append(adaa)
            if len(pred)>20:
                break
    pred=pred[:20]

    # remove already messaged ads
    tempp=copy.deepcopy(pred)
    if user_id in user_dic3:
        for elem in tempp: 
            if elem in user_dic3[user_id]:
                pred.remove(elem)

    # return top 10 ads
    return pred[:10]

# apply the method to each row
ser1=test_messages.apply(find_sim,axis=1)

# convert to submission format and write to csv
subdf=test_messages.copy()
subdf['ads']=ser1
subdf[['user_id','category_id','ads']].to_csv('ads_recommendation.csv', index=False)

print 'all tasks successfully completed'