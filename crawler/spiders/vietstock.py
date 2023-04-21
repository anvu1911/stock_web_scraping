"""
vietstock crawler
"""
import scrapy


def get_urls():
    ROOT_URL = "https://vietstock.vn/chung-khoan.htm"
    urls = []
    urls.append(ROOT_URL)

    return urls


class VietstockSpider(scrapy.Spider):
    name = 'vietstock'
    custom_settings = {
        'FEED_FORMAT': 'json',
        # 'FEED_URI': 'data/vietstock.json',
        'FEED_URI': 'data/vietstock_0421.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_INDE=NT': 4,
    }

    start_urls = get_urls()

    def parse(self, response):
        for article in response.css('div.single_post_text'):
            yield {
                'url': "https://vietstock.vn" + article.xpath('h4/a/@href').get(),
                'title': article.xpath('h4/a/@title').get(),
                'text': article.xpath('p/text()').get()
            }
