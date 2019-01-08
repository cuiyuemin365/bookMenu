from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from mydb.mydb import DBSession

Base = declarative_base()


class BookDetailInfo(Base):
    __tablename__ = 'book_detail_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    author_name = Column(String(100))
    press_name = Column(String(100))
    origin_book_name = Column(String(100))
    translator_name = Column(String(100))
    publish_year = Column(String(100))
    page_count = Column(String(100))
    price = Column(String(100))
    series_id = Column(String(100))
    series_name = Column(String(100))
    isbn = Column(String(100))
    score = Column(String(100))
    menu = Column(Text)
    tags = Column(Text)
    douban_id = Column(Integer)

    @staticmethod
    def add(item):
        session = DBSession()
        session.add(item)
        session.commit()
        session.close()

    @staticmethod
    def add_list(item_list):
        session = DBSession()
        session.add_all(item_list)
        session.commit()
        session.close()


class BookTableInfo(Base):
    __tablename__ = 'book_table_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    douban_id = Column(String(100))
    short_info = Column(String(300))
    img_url = Column(String(100))
    from_tag_id = Column(String(100))

    @staticmethod
    def add_list(item_list):
        session = DBSession()
        session.add_all(item_list)
        session.commit()
        session.close()


class BookTag(Base):
    __tablename__ = 'book_tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))

    @staticmethod
    def add_if_absent(tag_name):
        session = DBSession()
        result = session.execute(
            'insert into book_tag(name) '
            'select :param1 from dual '
            'where not exists (select * from book_tag where name = :param1)',
            {'param1': tag_name})
        session.commit()
        session.close()
        return result

    @staticmethod
    def get_tag_by_name(tag_name):
        session = DBSession()
        return session.query(BookTag).filter(BookTag.name == tag_name).one()


if __name__ == '__main__':
    pass