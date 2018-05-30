import sys
import numpy as np
import pandas as pd
import mysql.connector as mycon

if len(sys.argv) <= 1:
    no_specific_user = True
    user_id = 0
else:
    no_specific_user = False
    user_id = sys.argv[1]

# 使用MySQL Connector/Python接口连接数据库
cnx = mycon.connect(user='matching_user', password='ZZqz@123456', host='116.62.60.195', database='bixin_test')
cursor = cnx.cursor()

query = ("SELECT user_id, nick_name FROM user")
cursor.execute(query)
names = {}
for user, nick_name in cursor:
    names[user] = nick_name

if no_specific_user:
    print('所有用户：')
    for j in names.values():
        print(j, end=' ')
    sys.exit(0)

query = ("SELECT nick_name, constellation, height, weight, now_city, college, description FROM user where user_id='" + user_id + "'")
cursor.execute(query)

for nick_name, constellation, height, weight, now_city, college, description in cursor:
    print('nick_name:', nick_name)
    print('constellation:', constellation)
    print('height:', height)
    print('weight:', weight)
    print('now_city:', now_city)
    print('college:', college)
    print('description:', description)


query = ("SELECT from_user_id FROM user_like where target_user_id='" + user_id + "'")
cursor.execute(query)

from_users = []
for from_user_id in cursor:
    from_users.append(from_user_id[0])

print('给Ta点赞的人', len(from_users), '人：')
for j in from_users:
    print(names[j], end=' ')





cursor.close()
cnx.close()
