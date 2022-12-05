import scrapy
from urllib.parse import urlencode
from steam_spider.items import SteamSpiderItem

queries = ['indie', 'strategy', 'minecraft']
# queries = ['adventure', 'sports_and_racing', 'horror']

class SpidersteamgameSpider(scrapy.Spider):
    name = 'SpiderSteamGame'
    allowed_domains = ['store.steampowered.com']

    def start_requests(self):
        for query in queries:
            for i in range(1, 3):
                url = 'https://store.steampowered.com/search/?' + urlencode({'g': 'n', 'SearchText': query, 'page': i})
                yield scrapy.Request(url=url, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = response.css('a[class = "search_result_row ds_collapse_flag "]::attr(href)').extract()
        for product in products:
            yield scrapy.Request(url=product, callback=self.parse_product_page)

    def parse_product_page(self, response):
        items = SteamSpiderItem()
        game_name = response.css('span[itemprop="name"]::text').extract()
        date_of_release = response.css('div[class="date"]::text').extract()
        categories = response.css('span[data-panel] a::text').extract()
        rating = response.css('span[class = "responsive_reviewdesc_short"]::text').extract()
        developers = response.css('div[id="developers_list"] a::text').extract()
        tags = response.css('a[class="app_tag"]::text').extract()
        price = response.css('div[class="game_purchase_price price"]::text').extract()
        platforms = response.css('div[class="sysreq_tabs"] div::text').extract()
        if not game_name or int(''.join(date_of_release).strip()[-4::]) <= 2000:
            return
        if rating:
            rating = rating[0]
        if price:
            price = price[0]
        items['game_name'] = ''.join(game_name).strip()
        items['categories'] = ', '.join(map(lambda x: x.strip(), categories)).strip()
        items['rating'] = ''.join(rating).strip().replace('(', '').replace(')', '')
        items['date_of_release'] = ''.join(date_of_release).strip()
        items['developers'] = ', '.join(map(lambda x: x.strip(), developers)).strip()
        items['tags'] = ', '.join(map(lambda x: x.strip(), tags)).strip()
        items['price'] = ''.join(price).strip().replace('уб', '')
        if not platforms:
            platforms = response.xpath(
                '//div[@class="game_area_purchase_game" or @class="game_area_purchase_game "]/div/span/@class').extract()
            if platforms:
                platforms = platforms[0]
            items['platforms'] = ''.join(platforms).strip().replace('platform_img ', '')
        else:
            items['platforms'] = ', '.join(map(lambda x: x.strip(), platforms)).strip()
        yield items
