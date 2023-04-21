"""
cafef crawler
"""
import scrapy


def get_urls():
    ROOT_URL = "https://cafef.vn/thi-truong-chung-khoan.chn"
    urls = []
    urls.append(ROOT_URL)

    return urls


class CafefSpider(scrapy.Spider):
    name = 'cafef'
    custom_settings = {
        'FEED_FORMAT': 'json',
        # 'FEED_URI': 'data/cafef.json',
        'FEED_URI': 'data/cafef_0421.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_INDE=NT': 4,
    }

    start_urls = get_urls()

    def parse(self, response):
        for article in response.css('div.tlitem'):
            link = "https://cafef.vn" + article.xpath('h3/a/@href').get()
            request = scrapy.Request(url=link, callback=self.parse_article)
            request.meta['data'] = {
                'url': "https://cafef.vn" + article.xpath('h3/a/@href').get(),
                'title': article.xpath('h3/a/text()').get(),
                'text': article.css('p.sapo::text').get()
            }
            yield request
            # yield {
            #     'url': "https://cafef.vn" + article.xpath('h3/a/@href').get(),
            #     'title': article.xpath('h3/a/text()').get(),
            #     'text': article.css('p.sapo::text').get()
            # }

    def parse_article(self, response):
        data = response.meta.get('data')
        paragraphs = response.css('div.detail-content > p::text').getall()
        non_empty_paragraphs = list(filter(lambda s: s.strip() != "", paragraphs))
        stripped_paragraphs = list(map(lambda s: s.strip(), non_empty_paragraphs))
        content = ' '.join(stripped_paragraphs)
        data['content'] = content
        yield data