from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import Config
from sqlalchemy.orm import scoped_session

cfg = Config.get_cfg()
param = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' % (
    cfg.get('db', 'user'),
    cfg.get('db', 'password'),
    cfg.get('db', 'host'),
    cfg.get('db', 'port'),
    cfg.get('db', 'db')
)
engine = create_engine(param)
session_factory = sessionmaker(bind=engine)
DBSession = scoped_session(session_factory)

if __name__ == '__main__':
    pass
