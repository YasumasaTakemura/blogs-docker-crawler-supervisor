# -*- coding: utf-8 -*-
from flask import Flask
from app.db import view as db

app = Flask(__name__)

modules_define = [db.app]
for _app in modules_define:
    app.register_blueprint(_app)