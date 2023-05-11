from scrapy.exceptions import DropItem
from mysql.connector import connect
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os

load_dotenv()


class ChocolatePipeline:
    def __init__(self) -> None:
        self.create_conn()
        self.create_table()

    def create_conn(self):
        self.conn = connect(
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASS"],
            host=os.environ["MYSQL_HOST"],
            database=os.environ["MYSQL_DB"],
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS products;""")
        self.curr.execute(
            """
            CREATE TABLE products (
            id INT NOT NULL AUTO_INCREMENT,
            nombre VARCHAR(100),
            precio FLOAT,
            url VARCHAR(150),
            PRIMARY KEY(id));
            """
        )

    def store_items(self, item):
        self.curr.execute(
            """INSERT INTO products (nombre, precio, url) VALUES (%s, %s, %s)""",
            (item["nombre"], item["precio"], item["url"]),
        )
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_items(item)
        return item

    def close_spider(self, spider):
        self.conn.close()


class PriceToUSDPipeline:
    gbpToUsdRate = 1.26

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get("precio"):
            precioFloat = float(adapter["precio"])
            adapter["precio"] = precioFloat * self.gbpToUsdRate
            return item
        else:
            raise DropItem(f"Precio no encontrado en: {item}")


class DuplicatesPipeline:
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["nombre"] in self.names_seen:
            raise DropItem(f"Dato duplicado en: {item!r}")
        else:
            self.names_seen.add(adapter["nombre"])
            return item
