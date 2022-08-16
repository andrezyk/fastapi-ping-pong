import os
import time
import logging
from multiprocessing import Process

import requests
import uvicorn as uvicorn
from fastapi import FastAPI

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

app = FastAPI()


def call_ping():
    time.sleep(5)
    logging.info("Calling ping process")

    service_ping = os.getenv("SERVICE_PING_URI") or "http://localhost:8146"

    if not service_ping:
        logging.warning("SERVICE_PING_URI env var not set. Pong service cannot work!")

    while True:
        time.sleep(5)
        logging.info(f"Calling ping service {service_ping}/ping")
        res = requests.get(f"{service_ping}/ping")

        if not res.ok:
            logging.warning("Ping service didn't respond properly")

        logging.info(res.json())


@app.get("/pong")
async def root():
    return {"message": "pong"}


if __name__ == "__main__":
    logging.info("Starting pong app")

    up = Process(target=uvicorn.run, kwargs={'app': 'pong:app',
                                             'host': os.getenv("HOST") or "localhost",
                                             'port': os.getenv("PORT") or 8046})

    cp = Process(target=call_ping)

    up.start()
    cp.start()
