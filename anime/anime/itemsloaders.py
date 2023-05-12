from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


class AnimeLoader(ItemLoader):
    default_output_processor = TakeFirst()
    tipo_in = MapCompose(lambda x: x.replace("\n", "").strip())
    eps_in = MapCompose(lambda x: x.replace(" Eps,", "").replace(" Ep,", "").replace(",", "").strip())
    fechaEst_in = MapCompose(lambda x: x[-4:])
