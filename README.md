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


1、XML应用 （可以输入一个用户名来得到该用户的相关信息。 首先利用SQL查询关系数据库中该用户的信息（包括基本信息和发帖回帖信息） ，然后将这些信息封装在一份XML文档中，该XML文档遵循上述DTD描述。 ）

2、实现查询、触发器 （总共11个功能）

3、约束条件（不知道 sql 和 slack 里怎么搞 foreign key）

4、关系模式的规范化

5、点赞数功能
