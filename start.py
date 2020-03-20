from flask import Flask, render_template
from flask import request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Album, Artist

app = Flask(__name__)

engine = create_engine('sqlite:///spotify.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods=['GET'])
def index():
    albums = session.query(Album).all()
    return render_template('index.html', title='Albums', albums=albums)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5001)
