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


1、实现查询、触发器 （总共11个功能）

2、约束条件

3、关系模式的规范化

4、点赞数功能
