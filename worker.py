import requests
from json import loads, dumps
from GPT import GPT
from Redis import Redis
from logger import logging
import os
from dotenv import load_dotenv
import json

load_dotenv()
LIMIT = 2


class Worker:

    def process_message(self, db, message_json: str, redisObj: Redis, gptObj: GPT):
        payload = loads(message_json)
        res, status = gptObj.ask_bot(payload['query'])
        if status != 401:
            logging.info(" query process successful ")
            logging.info(res)
            url = "https://server.gallabox.dev/devapi/messages/whatsapp"
            data = {
                "channelId": os.getenv('CHANNEL_ID'),
                "channelType": "whatsapp",
                "recipient": {
                    "name": payload['name'],
                    "phone": payload['phone']
                },
                "whatsapp": {
                    "type": "text",
                    "text": {
                        "body": res['response']
                    }
                }
            }
            headers = {
                'apiKey': os.getenv('API_KEY_GB'),
                'apiSecret': os.getenv('API_SECRET_GB'),
                'Content-Type': 'application/json'
            }
            # payload['res'] = data
            data = json.dumps(data)
            # print(type(data))
            r = requests.post(url, data=data, headers=headers)
            # print(r.reason)
            # print(r.text)
            # print(r.content)
            logging.info(r)
        elif payload['count'] < LIMIT:
            payload['count'] = payload['count']+1
            message_json = dumps(payload)
            redisObj.queue_push(db, message_json)
            logging.warning("Processing failed - requeuing...")
            logging.warning(res)
        else:
            logging.error("Processing failed Attempted requeuing > LIMIT")
            logging.warning(res)


def main():
    redisObj = Redis()
    workerObj = Worker()
    gptObj = GPT()
    db = redisObj.redis_db()
    while True:
        message_json = redisObj.queue_pop(db)
        workerObj.process_message(db, message_json, redisObj, gptObj)


if __name__ == '__main__':
    main()
