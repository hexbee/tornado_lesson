# coding:utf8
from sqlalchemy import create_engine

HOSTNAME='106.14.212.108'
PORT='3306'
DATABASE='tornado_db'
USERNAME='admin'
PASSWORD='Admin@123'

db_url='mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, DATABASE)
engine = create_engine(db_url)

# 创建映像
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)

# 创建会话
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)
session = Session()


if __name__ == '__main__':
    print(dir(engine))
    print('---Base---', dir(Base))
    print('---session---', dir(session))
