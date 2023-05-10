from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class ChocolateProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    nombre_in = MapCompose(lambda x: x.lower())
    precio_in = MapCompose(
        lambda x: x.replace('<span class="price">\n', "")
        .replace('              <span class="visually-hidden">Sale price', "")
        .replace("</span>", "")
        .replace('<span class="price price--highlight">\n', "")
        .replace("\n", "")
        .replace("From ", "")
        .split("£")[-1]
    )
    url_in = MapCompose(lambda x: "https://www.chocolate.co.uk" + x)
