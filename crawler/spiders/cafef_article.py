"""
cafef crawler
"""
import scrapy


def get_urls():
    ROOT_URL = "https://cafef.vn/khoi-ngoai-mua-rong-khop-lenh-hon-10000-ty-dong-trong-quy-1-hai-co-phieu-nganh-thep-dan-dau-danh-sach-duoc-gom-nhieu-nhat-188230401092627688.chn"
    urls = []
    urls.append(ROOT_URL)

    return urls


class CafefSpier(scrapy.Spider):
    name = 'cafef_article'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data/cafef_article.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_INDE=NT': 4,
    }

    start_urls = get_urls()

    def parse(self, response):
        yield {
            'content': response.css('div.detail-content > p::text').getall(),
        }

