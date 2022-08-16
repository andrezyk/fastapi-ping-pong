import os
import time
import logging
from multiprocessing import Process

import requests
import uvicorn as uvicorn
from fastapi import FastAPI

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

app = FastAPI()


def call_pong():
    time.sleep(5)
    logging.info("Starting pong call process")

    service_pong = os.getenv("SERVICE_PONG_URI") or "http://localhost:8046"

    if not service_pong:
        logging.warning("SERVICE_PONG_URI env var not set. Pong service cannot work!")

    while True:
        time.sleep(5)
        logging.info("Calling pong service")
        res = requests.get(f"{service_pong}/pong")

        if not res.ok:
            logging.warning("Pong service didn't respond properly")

        logging.info(res.json())


@app.get("/ping")
async def root():
    return {"message": "ping"}


if __name__ == "__main__":
    logging.info("Starting ping app")

    up = Process(target=uvicorn.run, kwargs={'app': 'ping:app',
                                             'host': os.getenv("HOST") or "localhost",
                                             'port': os.getenv("PORT") or 8146})

    cp = Process(target=call_pong)

    up.start()
    cp.start()
