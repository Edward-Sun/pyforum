# pyforum
PKU Database Project

### How to start

Create a new environment

```bash
conda create -n <new-env-name>
```


install packages from requirement.txt

```bash
pip install -r requirement.txt
```

install frontend dependencies

```bash
cd static
sudo apt-get update
apt-get install npm
npm config set strict-ssl false
npm install
```

install and run mysql (set root password as 123456)

```bash
sudo apt-get install mysql-server
bash reload_sql.sh
```

install and run redis

```bash
cd ..
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
cd pyforum
bash redis.sh
```

run backend at localhost:5000

```bash
python backend.py
```

#### TODO

~~1、user profile 没有弄（每位用户都有自己的基本信息，包括账号、 用户昵称、生日、 密码、 性别、年龄、 电子邮件、用户等级、注册日期等 ）~~

2、个人页面是用户近期信息的汇总，可能是近期发帖，这个也没有弄。

3、修改权限没有弄 （现在所有人都可以修改别人的帖子，其实就没有考虑权限，应该要只有管理员、版主、和原帖主可以修改）

4、板块没有弄版主（版主拥有对其所掌管版块的修改权限。可以修改版块信息， 可以对用户在该板块发帖和回帖内容进行删除操作。 ），也还没有弄板块介绍。

5、没有专门设计一个数据库管理员，我的想法是当前是每个板块有版主，权限很大，我们把整个论坛当作0号板块，改一改就可以算数据库管理员了。

6、数据库管理员可以增加或者删除用户、 帖子及回复。 这个还没有做。

7、XML应用 （看不懂要做什么）（可以输入一个用户名来得到该用户的相关信息。 首先利用SQL查询关系数据库中该用户的信息（包括基本信息和发帖回帖信息） ，然后将这些信息封装在一份XML文档中，该XML文档遵循上述DTD描述。 ）

8、实现查询、触发器及用户权限管理 （总共11个功能）

9、查询其他用户信息

10、约束条件（不知道 sql 和 slack 里怎么搞 foreign key）

11、关系模式的规范化
