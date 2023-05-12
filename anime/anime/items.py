import scrapy


class AnimeItem(scrapy.Item):
    nombre = scrapy.Field()
    tipo = scrapy.Field()
    eps = scrapy.Field()
    fechaEst = scrapy.Field()
