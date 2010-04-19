##
# Author: Flavio [FlaPer87] Percoco Premoli <flaper87@flaper87.org>
#

from pymongo.connection import Connection
from ghettoq.backends.base import BaseBackend
from ghettoq.messaging import Empty

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 27017

class MongodbBackend(BaseBackend):

    def establish_connection(self):
        self.port = self.port or DEFAULT_PORT
        self.host = self.host or DEFAULT_HOST
        self.connection = Connection(host=self.host, port=self.port)
        self.database = getattr(self.connection, (self.database == "/" and
"ghettoq") or (not self.database and "ghettoq") or self.database)
        col = getattr(self.database, "messages")
        col.ensure_index([("queue", 1)])
        return col

    def put(self, queue, message):
        self.client.insert({"payload" : message, "queue" : queue})

    def get(self, queue):
        msg =  self.client.find_one({"queue" : queue})
        if not msg:
            raise Empty, "Empty queue"
        self.client.remove(msg)
        return msg["payload"]

    def purge(self, queue):
        return self.client.remove({"queue" : queue})
