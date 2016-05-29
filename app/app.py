"""
The Lakbay app in Flask.

:Author:     Maded Batara III
:Version:    v2.0dev (2016-03-24)
"""

from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
