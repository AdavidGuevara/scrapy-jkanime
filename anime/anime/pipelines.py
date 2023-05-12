from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from mysql.connector import connect
from dotenv import load_dotenv
import os

load_dotenv()


class AnimePipeline:
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
        self.curr.execute("""DROP TABLE IF EXISTS animes;""")
        self.curr.execute(
            """
            CREATE TABLE animes (
            id INT NOT NULL AUTO_INCREMENT,
            nombre VARCHAR(500),
            tipo VARCHAR(75),
            eps INT,
            fechaEst INT,
            PRIMARY KEY(id));
            """
        )

    def store_items(self, item):
        self.curr.execute(
            """INSERT INTO animes (nombre, tipo, eps, fechaEst) VALUES (%s, %s, %s, %s)""",
            (item["nombre"], item["tipo"], item["eps"], item["fechaEst"]),
        )
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_items(item)
        return item

    def close_spider(self, spider):
        self.conn.close()


class ToInteger:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        adapter["eps"] = int(adapter["eps"])
        adapter["fechaEst"] = int(adapter["fechaEst"])
        return item
