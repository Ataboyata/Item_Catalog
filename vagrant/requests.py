from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
import json

app = Flask(__name__)

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def displayeverything():
    # This Page displays all categories and items
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog/<int:category_id>/Items')
def displayitems(category_id):
    # This Page displays items for a specific category
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).all()
    return render_template('items.html', categories=categories, items=items)


@app.route('/catalog/<int:category_id>/<int:item_id>')
def displayitem():
    # This Page displays the description of a specific item
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', item=item)

@app.route('/catalog/new', methods=['GET', 'POST'])
def createitem(category_name):
    # This Page creates a new item
    if request.method == 'POST':
        category = session.query(Category).filter_by(
            name=request.form['category_name']).one()
        item_to_create = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category.id)
        session.add(item_to_create)
        session.commit()
        return redirect(url_for('displayeverything', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


@app.route('/catalog/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def edititem(category_id, item_id):
    # This Page edits an item
    category = session.query(Category).filter_by(id=category_id).one()
    item_to_edit = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item_to_edit.name = request.form['name']
        if request.form['description']:
            item_to_edit.description = request.form['description']
        session.add(item_to_edit)
        session.commit()
        return redirect(url_for('displayeverything', category_id=category_id))
    else:
        return render_template('edititem.html', category_id=category_id, item_to_edit=item_to_edit)


@app.route('/catalog/<int:category_id>/<int:item_id>/delete',
    methods=['GET', 'POST'])
def deleteitem(category_id, item_id):
    # This Page deletes an item
    category = session.query(Category).filter_by(id=category_id).one()
    item_to_delete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        return redirect(
            url_for(
                'displayeverything',
                category_id=category_id,
                item_to_delete=item_to_delete))
    else:
        return render_template(
            'deleteitem.html',
            category_id=category_id,
            item_id=item_id)


@app.route('/catalog/<int:category_id>/JSON')
def itemsincategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(AllItems=[i.serialize for i in items])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
