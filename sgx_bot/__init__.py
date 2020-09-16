"""Load Config!"""
# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import sys
from pymongo import MongoClient

logger.info("Loading Configurations...")
#Use python >=3.8
if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    logger.error(
        "You MUST have a python version of at least 3.8! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get("TOKEN", "")
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    OWNER_ID = int(os.environ.get("OWNER_ID"))
    DB_URI = os.environ.get("DB_URI")
else:
    TOKEN = None
    APP_ID = None
    API_HASH = None
    OWNER_ID = None
    DB_URI = None

# Init Mongo
MONGOCLIENT = MongoClient(DB_URI, 27017, serverSelectionTimeoutMS=1)
MONGO = MONGOCLIENT.sgx_bot


def is_mongo_alive():
    try:
        MONGOCLIENT.server_info()
    except BaseException as e:
        print(e)
        return False
    return True    