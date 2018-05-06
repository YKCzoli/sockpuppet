#!/usr/bin/python

import json
import logging
import psycopg2
import pytz
from datetime import datetime

import tornado.gen
import tornado.options
import tornado.web
import tornado.websocket

from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import os
dbname = os.getenv("DBNAME")
user = os.getenv("USER")
host = os.getenv("HOST")
password = os.getenv("PASSWORD")
port = os.getenv("PORT")


def parse_payload(data):
    try:
        data_list = json.loads(data)
        parsed_json = (data_list[0].get("terms"), data_list[0].get("browser"))
        return parsed_json

    except Exception as ex:
        logging.exception(ex)

    return None, None


@tornado.gen.coroutine
def connect_and_read_websocket():

    connection = "dbname={} user={} host={} password={} port={}".format(dbname, user, host, password, port)
    url = "ws://dashboard.tpllabs.ca:4571/rtsearches"
    query = "INSERT INTO tpl_searches (terms, browser) VALUES (%s, %s);"

    try:
        logging.info("connecting to: %s", url)
        w = yield tornado.websocket.websocket_connect(url, connect_timeout=5)
        logging.info("connected to %s, waiting for messages", url)
    except Exception as ex:
        logging.error("couldn't connect, err: %s", ex)
        return

    while True:
        conn = psycopg2.connect(connection)
        cursor = conn.cursor()
        payload = yield w.read_message()
        if payload is None:
            logging.error("uh oh, we got disconnected")
            return

        if len(payload):
            try:
                logging.info(payload)
                data = parse_payload(payload)
                cursor.execute(query, data)
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                logging.exception(error)

        else:
            logging.warn("unknown paylod: %s", payload.decode('utf8'))


if __name__ == '__main__':
    tornado.options.define(name="ws_addr", type=str, help="Address of the websocket host to connect to.")
    tornado.options.parse_command_line()

    tornado.ioloop.IOLoop.instance().run_sync(connect_and_read_websocket)
