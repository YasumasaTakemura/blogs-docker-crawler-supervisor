# -*- coding: utf-8 -*-
import logging
import os
from flask import request, Blueprint, abort, jsonify
from .model import DBConnector, DMO, DDO
from app.store.store import Store

logger = logging.getLogger('DB_View')
table_name = os.environ.get('DATABASE_NAME') or 'crawler'

app = Blueprint('db', __name__)


@app.route('/', methods=['GET','POST'])
def working():
    return 'working', 200


@app.route('/create_table', methods=['POST'])
def create_table():
    db = DBConnector()
    ddo = DDO(db)
    try:
        ddo.create_table_crawler()
        return 'table created', 200
    except Exception as e:
        logger.error(e)
        abort(400, 'no tables created')


@app.route('/show_records', methods=['GET'])
def show_records():
    db = DBConnector()
    dmo = DMO(db)
    try:
        res = dmo.show(table=table_name)
        return jsonify(data=res)
    except Exception as e:
        logger.error(e)
        abort(400, )


@app.route('/get_next', methods=['GET'])
def get_next():
    db = DBConnector()
    dmo = DMO(db)
    path = dmo.get_next_path(table=table_name)
    return path or '', 200


@app.route('/add', methods=['POST'])
def push_urls():
    paths = request.form.getlist('path')
    logger.info(paths)
    db = DBConnector()
    dmo = DMO(db)
    records = dmo.apply_fields(paths)
    if dmo.push_paths(records, table=table_name):
        return jsonify(data=records), 200
    abort(400, '')


@app.route('/create_bucket', methods=['POST'])
def create_bucket():
    bucket_name = request.form.get('bucket_name')
    store = Store()
    bucket_name = store.create_bucket(bucket_name=bucket_name)
    if bucket_name:
        return bucket_name, 200
    abort(400, '')


@app.route('/upload_file', methods=['POST'])
def upload_file():
    data = request.form
    bucket_name = data.get('bucket_name')
    filename = data.get('filename')
    data = data.get('data')
    store = Store()
    filename = store.write(bucket_name=bucket_name, filename=filename, data=data)
    return filename, 200


@app.route('/upload', methods=['POST'])
def upload():
    data = request.form
    bucket = data.get('bucket_name')
    path = data.get('path')
    data = data.get('data')
    logger.info('{}'.format(path))
    store = Store()
    db = DBConnector()
    dmo = DMO(db)
    dmo.update_crawled_status(path, table_name)
    filename = store.write(bucket_name=bucket, filename=path, data=data)
    if filename:
        return filename, 200
    logger.error('not uploaded')
    abort(400, '')
