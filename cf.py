import numpy as np
import pandas as pd
import mysql.connector as mycon

# 使用MySQL Connector/Python接口连接数据库
cnx = mycon.connect(user='matching_user', password='ZZqz@123456', host='116.62.60.195', database='bixin_test')

# 用cursor执行数据库查询语句
cursor = cnx.cursor()
#query = ('SELECT from_user_id, target_user_id FROM user_like GROUP BY target_user_id, from_user_id')
query = ('SELECT from_user_id, target_user_id FROM user_like')
cursor.execute(query)

from_users = []
target_users = []
likes = []
for i, j in cursor:
    from_users.append(i)
    target_users.append(j)
    likes.append((i, j))
    #print(i, j)

from_users = list(set(from_users))
target_users = list(set(target_users))

# 把用户间的‘关注’行为存入数据框
data = np.zeros((len(from_users), len(target_users)))
df = pd.DataFrame(data, index=from_users, columns=target_users)

weight_likes = 1
for i, j in likes:
    df[j][i] = weight_likes
print(df)

# 将Pandas数据框保存到.csv文件中
df.to_csv('prefer.csv')

# 计算item相似度，用点积计算两个物品被关注的相似程度
def sim(src, dest):
    dot = np.sum(src*dest)
    return dot

def locate_key_index(elem):
    return elem[1]

# 创建item相似度数据框/矩阵
#data = np.zeros((len(target_users), len(target_users)))
#sim_matrix = pd.DataFrame(data, index=target_users, columns=target_users)
#for src in target_users:
    #for dest in target_users:
        #sim_matrix[dest][src] = sim(df[src], df[dest])

# 推荐
user = np.random.choice(from_users)
print('chosen user:', user)
record = []
recommend = dict()
for target in target_users:
    if df[target][user] > 0:
        record.append(target)
print('record:', record)

for item in record:
    for target in target_users:
        score = sim(df[item], df[target])
        if score > 0:
            if target in recommend and recommend[target][1] > score:
                continue
            recommend[target] = (target, score)

for i in record:
    if i in recommend:
        del recommend[i]

recommend_list = list(recommend.values())
recommend_list.sort(key=locate_key_index, reverse=True)

print('recommend:', recommend_list)
print('length of recommend:', len(recommend_list))

cursor.close()
cnx.close()
