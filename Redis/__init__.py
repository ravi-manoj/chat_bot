import json
import redis
import os
from Query import Query
from logger import logging
from dotenv import load_dotenv

load_dotenv()
class Redis:
    def redis_db(self):
        db = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            password=os.getenv('REDIS_PASS'),
            ssl=True
        )
        db.ping()
        return db

    def add_query(self, query: Query):
        db = self.redis_db()
        message_json = json.dumps(query.__dict__)
        self.queue_push(db, message_json)

    def queue_push(self, db, message):
        db.lpush("msg_q", message)
        logging.info("item pushed into queue")
        logging.info(message)

    def queue_pop(self, db):
        _, message_json = db.brpop("msg_q")
        logging.info("item popped from queue")
        logging.info(message_json)
        return message_json
