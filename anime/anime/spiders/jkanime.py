from ..itemsloaders import AnimeLoader
from ..items import AnimeItem
import scrapy


class JkanimeSpider(scrapy.Spider):
    name = "jkanime"
    allowed_domains = ["jkanime.net"]

    def get_url(self, offset=1):
        return f"https://jkanime.net/directorio/{offset}/"

    def start_requests(self):
        yield scrapy.Request(
            url=self.get_url(), callback=self.parse, meta={"offset": 1}
        )

    def parse(self, response):
        offset = response.meta["offset"]
        animes = response.css("div.custom_item2")
        for anime in animes:
            single_anime = AnimeLoader(AnimeItem(), anime)
            single_anime.add_css("nombre", "h5.card-title a::text")
            single_anime.add_css("tipo", "p.card-txt::text")
            single_anime.add_css("eps", "p.ep::text")
            single_anime.add_css("fechaEst", "small.text-muted::text")
            yield single_anime.load_item()

        next = response.xpath("//a[contains(@class, 'nav-next')]").get()
        if next:
            yield scrapy.Request(
                url=self.get_url(offset=offset + 1),
                callback=self.parse,
                meta={"offset": offset + 1},
            )
