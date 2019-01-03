import config
from faker import Faker
fake = Faker("zh_CN")

import random
with open('add_fake_data.sql', 'w') as fout:
    fout.write("USE "+config.MYSQL_NAME+";\n")
    for i in range(100):
        fout.write("INSERT INTO `user` (`username`,`email`,`password_hash`,`confirmed`,`register_date`)\
VALUES ('user"+str(i)+"', 'qq"+str(i)+"@qq.com',\
'pbkdf2:sha1:1000$sheKmza5$95de7e0052f2dd2b533570a8c6850fee9a0c9ea4', '1', UNIX_TIMESTAMP());\n")
    
    fout.write("insert into module(parent_id,name,url,weight) values(0,'版块4','/module/4',600);\n")
    fout.write("insert into module(parent_id,name,url,weight) values(0,'版块5','/module/5',500);\n")
    fout.write("insert into module(parent_id,name,url,weight) values(0,'版块6','/module/6',400);\n")
    fout.write("insert into module(parent_id,name,url,weight) values(0,'版块7','/module/7',300);\n")
    
    for i in range(200):
        user_id = random.randint(1,101)
        module_id = random.randint(3,7)
        read_count = random.randint(0,100)
        fout.write("INSERT INTO `post` (`title`,`user_id`,`module_id`,`content`, \
`created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`) \
VALUES ('测试"+str(i)+"标题:"+''.join(fake.words(nb=3))+"',"+str(user_id)+","+str(module_id)+",'测试"+str(i)+"内容:"+fake.text(max_nb_chars=50)+"',\
UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),"+str(read_count)+","+str(random.randint(0,read_count))+");\n")
    
    floor_num = {}
    for i in range(2,201):
        floor_num[i] = 1
        
    for i in range(1200):
        user_id = random.randint(1,101)
        post_id = random.randint(2,200)
        floor_num[post_id] += 1
        
        fout.write("UPDATE `post` SET `comment_floor` = "+str(floor_num[post_id])+" WHERE `id` = "+str(post_id)+";\n")
        
        fout.write("INSERT INTO `reply` (`user_id`,`post_id`,`content`,\
`created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor_num`) \
VALUES ("+str(user_id)+","+str(post_id)+",'回复"+str(i)+"内容:"+fake.text(max_nb_chars=50)+"',UNIX_TIMESTAMP(),\
UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,"+str(floor_num[post_id])+");\n")