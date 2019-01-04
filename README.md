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

1、点赞功能
