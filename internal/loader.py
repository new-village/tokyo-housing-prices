""" loader.py
"""
import os
from datetime import datetime
from azure.cosmos import CosmosClient, exceptions, PartitionKey


class connection():
    def __init__(self, table):
        # Create the client
        url = os.environ['ACCOUNT_URI']
        key = os.environ['ACCOUNT_KEY']
        client = CosmosClient(url, credential=key)

        # Create or Get Database
        try:
            self.database = client.create_database('tokyo-housing-prices')
        except exceptions.CosmosResourceExistsError:
            self.database = client.get_database_client('tokyo-housing-prices')

        # Create or Get Container
        try:
            self.container = self.database.create_container(id=table, partition_key=PartitionKey(path='/_id'))
        except exceptions.CosmosResourceExistsError:
            self.container = self.database.get_container_client(table)
        except exceptions.CosmosHttpResponseError:
            raise

    def count(self):
        count = list(self.container.read_all_items()).__len__()
        return count

    def select_all(self):
        items = list(self.container.read_all_items())
        for i in items:
            [i.pop(key, 'x') for key in ['_rid', '_self', '_etag', '_attachments', '_ts']]
        return items

    def get(self, id):
        return self.container.read_item(id)

    def upsert(self, items):
        for i in items:
            self.container.upsert_item(i)

    def start(self, pid):
        self.container.upsert_item({'id': pid, 'start': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'status': 'Processing'})

    def finish(self, pid, status):
        self.container.upsert_item({'id': pid, 'end': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'status': status})
