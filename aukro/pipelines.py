# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class AukroPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.connection = sqlite3.connect("../db.db")
        # self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS items(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        link TEXT,
                        category TEXT,
                        dead_line DATETIME,
                        max_bid INTEGER,
                        total_price INTEGER,
                        top_item_id TEXT,
                        top_item_price INTEGER,
                        top_item_quantity INTEGER,
                        top_item_description TEXT,
                        top_item_img TEXT
                        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.cursor.execute("SELECT * FROM items WHERE name=?", (item["name"], ))
        if self.cursor.fetchone() is None:
            self.cursor.execute("""INSERT INTO items VALUES (:id, :name, :link, :category, :dead_line, :max_bid, 
            :total_price, :top_item_id, :top_item_price, :top_item_quantity, :top_item_description, 
            :top_item_img)""", {"id": None, "name": item["name"],
                    "link": item["link"], "category": item["category"], "dead_line": item["dead_line"],
                    "max_bid": item["max_bid"], "total_price": item["total_price"], "top_item_id": item["top_item_id"],
                    "top_item_price": item["top_item_price"], "top_item_quantity": item["top_item_quantity"],
                    "top_item_description": item["top_item_description"], "top_item_img": item["top_item_img"]})
        else:
            self.cursor.execute("""UPDATE items SET max_bid= :max_bid
                                    WHERE name= :name""", {"max_bid": item["max_bid"], "name": item["name"]})

        self.connection.commit()