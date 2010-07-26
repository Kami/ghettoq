import unittest

from anyjson import serialize, deserialize

from ghettoq.simple import Connection, Empty


def create_connection(database):
    return Connection("mongodb", host="localhost", database=database)


class TestMongoDbBackend(unittest.TestCase):
    
    def setUp(self):
        self.conn = create_connection("database")
        self.q = self.conn.Queue("testing")
    
    def tearDown(self):
        self.q.purge()

    def test_empty_raises_Empty(self):
        self.assertRaises(Empty, self.q.get)

    def test_queue_is_empty_after_purge(self):
        self.q.put(serialize({"name": "George Constanza"}))
        self.q.put(serialize({"name": "George Constanza"}))
        self.q.purge()

        self.assertRaises(Empty, self.q.get)

    def test_put_and_get(self):
        self.q.put(serialize({"name": "George Constanza"}))
        self.q.put(serialize({"name": "George Constanza"}))

        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza"})
        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza"})
        self.assertRaises(Empty, self.q.get)
        
    def test_specified_priority(self):
        self.q.put(serialize({"name": "George Constanza 1"}))
        self.q.put(serialize({"name": "George Constanza 2"}), 1)
        self.q.put(serialize({"name": "George Constanza 3"}), 2)
        self.q.put(serialize({"name": "George Constanza 4"}), 3)
        self.q.put(serialize({"name": "George Constanza 5"}), 0)
        self.q.put(serialize({"name": "George Constanza 6"}))
        
        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza 6"})
        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza 5"})
        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza 1"})
        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza 2"})
        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza 3"})
        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza 4"})
        
        self.assertRaises(Empty, self.q.get)
        
    def test_default_priority(self):
        self.q.put(serialize({"name": "George Constanza 1"}))
        self.q.put(serialize({"name": "George Constanza 2"}))
        
        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza 2"})
        self.assertEquals(deserialize(self.q.get()),
                {"name": "George Constanza 1"})
        
        self.assertRaises(Empty, self.q.get)
        
    def test_empty_queset_raises_Empty(self):
        a, b, c, = self.conn.Queue("a"), self.conn.Queue("b"), self.conn.Queue("c")
        self.queueset = self.conn.QueueSet(queue.name for queue in (a, b, c))
        for self.queue in a, b, c:
            self.assertRaises(Empty, self.queue.get)
        self.assertRaises(Empty, self.queueset.get)