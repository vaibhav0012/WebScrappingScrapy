# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import sqlite3

from itemadapter import ItemAdapter
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus


username = quote_plus('user_name')  # Replace with your MongoDB username
password = quote_plus('Password')     # Replace with your MongoDB password, encoded
cluster = 'cluster_name'  # Replace with your cluster name
authSource = 'admin'  # Default authentication source in MongoDB Atlas
authMechanism = 'SCRAM-SHA-1'  # Default mechanism used by MongoDB Atlas
dbName = 'DB_Name'  # Replace with your database name
collName = 'Collection_name'  # Replace with your collection name

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

class SQLitePipeline:

    def open_spider(self, spider):
        # create database file
        self.connection = sqlite3.connect('transcripts.db')
        # we need a cursor object to execute SQL queries
        self.c = self.connection.cursor()
        #  try/except will help when running this for the +2nd time (we can't create the same table twice)
        try:
            # query: create table with columns
            self.c.execute('''
                CREATE TABLE transcripts(
                    title TEXT,
                    author TEXT,
                    length TEXT
                )
            ''')
            # save changes
            self.connection.commit()
        except sqlite3.OperationalError:
            pass


    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # query: insert data into table
        self.c.execute('''
            INSERT INTO transcripts (title,author,length) VALUES(?,?,?)
        ''', (
            item.get('title'),
            ', '.join(item.get('author', [])) if isinstance(item.get('author'), list) else item.get('author', 'Unknown Author'),
            item.get('length')
        ))
        # save changes
        self.connection.commit()
        return item