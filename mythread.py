# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import sys
import re
from decimal import Decimal
import json
import threading
from myredis.myredis import *
from time import sleep
from model.model import *
from log.log import logger

reload(sys)
sys.setdefaultencoding('utf-8')

from sqlalchemy.ext.declarative import DeclarativeMeta

headers = {
    'Host': 'book.douban.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


detail_url = 'https://book.douban.com/subject/%s'


class TablePageThread(threading.Thread):

    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.name = thread_name
        self.redis_con = MyRedis.get_con()

    def entrance(self):
        while 1:
            if int(self.redis_con.llen(QUEUE_DOUBAN_TAG)) == 0:
                logger.info(self.name + " is sleeping")
                sleep(3)
                logger.info(self.name + " is running")
            else:
                tag_name = str(self.redis_con.rpop(QUEUE_DOUBAN_TAG).decode('utf-8'))
                handle_tag(self.redis_con, tag_name)

    def run(self):
        logger.info(self.name + " begin run")
        self.entrance()


class DetailPageThread(threading.Thread):

    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.name = thread_name
        self.redis_con = MyRedis.get_con()

    def entrance(self):
        while 1:
            if int(self.redis_con.llen(QUEUE_DOUBAN_ID)) == 0:
                logger.info(self.name + " is sleeping")
                sleep(3)
                logger.info(self.name + " is running")
            else:
                douban_id = str(self.redis_con.rpop(QUEUE_DOUBAN_ID).decode('utf-8'))
                handle_douban_id(self.redis_con, douban_id)

    def run(self):
        logger.info(self.name + " begin run")
        self.entrance()


def fetch_author_name(soup):
    result = (lambda x: x.next_sibling.next_sibling.text.strip() if x is not None else None)(
        soup.find('span', text='作者:'))
    if result is not None:
        return result
    return '|'.join(
        map(
            lambda x: x.text.strip(),
            (lambda x: x.parent.find_all('a') if x is not None else None)(soup.find('span', text=' 作者'))
        )
    )


def handle_douban_id(redis_con, douban_id):
    try:
        logger.info('id %s' % douban_id)
        url = detail_url % douban_id
        # url = '/data/project/self/bookMenu/detail.html'
        response_text = get_page_content(url)
        # response_text = open('/data/project/self/bookMenu/detail.html', 'r').read()
        soup = get_soup(response_text)
        info = BookDetailInfo()
        info.name = soup.find(attrs={'property': 'v:itemreviewed'}).text.strip()
        info.author_name = fetch_author_name(soup)
        info.press_name = (lambda x: x.next_sibling.strip() if x is not None else None)(
            soup.find('span', string='出版社:'))
        info.origin_book_name = (lambda x: x.next_sibling.strip() if x is not None else None)(
            soup.find('span', string='原作名:'))
        info.translator_name = (lambda x: x.next_sibling.next_sibling.text.strip() if x is not None else None)(
            soup.find('span', string=' 译者'))
        info.page_count = (lambda x: x.next_sibling.strip() if x is not None else None)(
            soup.find('span', string='页数:'))
        info.price = (lambda x: x.next_sibling.strip() if x is not None else None)(
            soup.find('span', string='定价:'))
        tag_a_2 = soup.find('a', attrs={'href': re.compile("https://book.douban.com/series/")})
        info.series_id = (lambda x: x['href'].split('/')[-1] if x is not None else None)(tag_a_2)
        info.series_name = (lambda x: x.text.strip() if x is not None else None)(tag_a_2)
        info.isbn = (lambda x: x.next_sibling.strip() if x is not None else None)(
            soup.find('span', string='ISBN:'))
        info.publish_year = (lambda x: x.next_sibling.strip() if x is not None else None)(
            soup.find('span', string='出版年:'))
        info.score = (lambda x: Decimal(x.text.strip()) if x is not None else None)(
            soup.find(attrs={'property': 'v:average'}))
        info.menu = (lambda x: x.text.strip() if x is not None else None)(
            soup.find(attrs={'id': 'dir_' + douban_id + '_full'}))
        info.tags = '|'.join(map(lambda x: x.text.strip(), soup.find_all('a', attrs={'href': re.compile("/tag/")})))
        info.douban_id = douban_id
        logger.info(
            json.dumps(info, sort_keys=True, indent=2, cls=AlchemyEncoder, encoding='utf-8', ensure_ascii=False))
        BookDetailInfo.add(info)
    except Exception as e:
        logger.error('--->%s', e)
        redis_con.lpush(QUEUE_DOUBAN_ID_EXCEPTION, douban_id)


def get_page_content(url):
    response = requests.get(url, headers=headers)
    return response.text


def get_soup(text):
    return BeautifulSoup(text,
                         'html.parser',
                         from_encoding='utf-8'
                         )


def handle_tag(redis_con, tag_name):
    logger.info('handle%s', tag_name)
    try:
        BookTag.add_if_absent(tag_name)
        i = 0
        while True:
            start = 20 * i
            url = 'https://book.douban.com/tag/%s?start=%s&type=T' % (tag_name, start)
            logger.info(url)
            text = get_page_content(url)
            if not text.find('没有找到符合条件的图书') < 0:
                logger.info('finished:' + tag_name)
                break
            if text.find('豆瓣图书标签') < 0:
                raise Exception('列表页面异常' + text)
            soup = get_soup(text)
            item_list = []
            for item in soup.find_all(class_='subject-item'):
                info = BookTableInfo()
                info.name = item.find(title=True)['title']
                info.douban_id = item.find(title=True)['href'].split('/')[-2]
                info.short_info = item.find(class_='pub').text.strip()
                info.img_url = item.find('img')['src']
                info.from_tag_id = BookTag.get_tag_by_name(tag_name).id
                item_list.append(info)
            redis_con.lpush(QUEUE_DOUBAN_ID, map(lambda x: x.douban_id, item_list))
            BookTableInfo.add_list(item_list)
            i += 1
    except Exception as e:
        logger.error('---->%s', e)
        redis_con.lpush(QUEUE_DOUBAN_TAG_EXCEPTION, tag_name)


if __name__ == '__main__':
    pass
