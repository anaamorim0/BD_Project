#! /usr/bin/python3
import logging

import db
from app import APP

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    db.connect()
    APP.run(host='0.0.0.0', port=9001)
