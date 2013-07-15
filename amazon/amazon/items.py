# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class AmazonItem(Item):
    rank = Field()
    name = Field()
    url = Field()
    image = Field()
    price = Field()
    pass