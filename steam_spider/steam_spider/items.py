import scrapy


class SteamSpiderItem(scrapy.Item):
    game_name = scrapy.Field()
    categories = scrapy.Field()
    rating = scrapy.Field()
    date_of_release = scrapy.Field()
    developers = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()