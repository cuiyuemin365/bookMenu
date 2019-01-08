import requests

headers = {
    'Host': 'book.douban.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

proxies = {
    'http': 'http://119.101.118.38:9999',
    'https': 'http://119.101.118.38:9999'
}


def get_page_content(url):
    response = requests.get(url, headers=headers, proxies=proxies)
    return response.text


if __name__ == '__main__':
    print get_page_content('https://book.douban.com/')
