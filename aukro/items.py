# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AukroItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    dead_line = scrapy.Field()
    max_bid = scrapy.Field()
    total_price = scrapy.Field()
    top_item_id = scrapy.Field()
    top_item_price = scrapy.Field()
    top_item_quantity = scrapy.Field()
    top_item_description = scrapy.Field()
    top_item_img = scrapy.Field()
