from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Category, Item
import json

app = Flask(__name__)

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog')
def displayeverything():
	#This Page displays all categories and items


@app.route('/catalog/<int:category_id>/Items')
def displayitems():
    #This Page displays items for a specific category


@app.route('/catalog/<int:category_id>/<int:item_id>')
def displayitem():
    #This Page displays the description of a specific item


@app.route('/catalog/new', methods=['GET', 'POST'])
def createitem():
    #This Page creates a new item


@app.route('catalog/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def edititem():
    #This Page edits an item

@app.route('catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteitem():
    #This Page deletes an item


@app.route('catalog/<int:category_id>/JSON')
def itemsincategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def itemJSON(category_id,item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(AllItems=[i.serialize for i in items])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)