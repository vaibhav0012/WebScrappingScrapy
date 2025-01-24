# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus


username = quote_plus('<user_name>')  # Replace with your MongoDB username
password = quote_plus('<password>')     # Replace with your MongoDB password, encoded
cluster = '<cluster_name>'  # Replace with your cluster name
authSource = 'admin'  # Default authentication source in MongoDB Atlas
authMechanism = 'SCRAM-SHA-1'  # Default mechanism used by MongoDB Atlas
dbName = '<dbname>'  # Replace with your database name
collName = '<collection_name>'  # Replace with your collection name

# Construct the URI
uri = (
    'mongodb+srv://' + username + ':' + password +
    '@' + cluster + '/?authSource=' + authSource +
    '&authMechanism=' + authMechanism
)

class MongodbPipeline:
    collection_name = 'Audible_Books'
    def open_spider(self, spider):
        self.client = MongoClient(uri)
        self.db = self.client['My_Database']
        logging.warning('Spider Open - Pipeline')

    def class_spider(self, spider):
        self.client.close()
        logging.warning('Spider Closing - Pipeline')
        pass

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
