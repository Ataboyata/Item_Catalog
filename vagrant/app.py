from flask import Flask, render_template, request, redirect
from flask import url_for, jsonify, make_response, g, flash
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

from functools import wraps
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
import httplib2
import requests
import json

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///item_catalog.db', encoding='utf-8')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Creates a login required function to be used repeatedly for authentication
# in other code
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state token
@app.route('/login')
def login():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate anti-forgery state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps(
                'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # See if user exists
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return "Login Successful"


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/catalog')
def displayeverything():
    # This Page displays all categories and items
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog/<int:category_id>')
def displayitems(category_id):
    # This Page displays items for a specific category
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', categories=categories, items=items)


@app.route('/catalog/item/<int:item_id>')
def displayitem(item_id):
    # This Page displays the description of a specific item
    item = session.query(Item).filter_by(id=item_id).one_or_none()
    return render_template('item.html', item=item)


@app.route('/catalog/item/new', methods=['GET', 'POST'])
@login_required
def createitem():
    # This Page creates a new item
    if request.method == 'POST':
        item_to_create = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category_id'],
            user_id=login_session['user_id'])
        session.add(item_to_create)
        session.commit()
        return redirect(url_for('displayeverything'))
    else:
        return render_template('newitem.html')


@app.route('/catalog/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edititem(item_id):
    # This Page edits an item
    item_to_edit = session.query(Item).filter_by(id=item_id).one_or_none()
    if item_to_edit.user_id != login_session['user_id']:
        return redirect(url_for('displayeverything'))
    if request.method == 'POST':
        if request.form['name']:
            item_to_edit.name = request.form['name']
        if request.form['description']:
            item_to_edit.description = request.form['description']
        if request.form['category_id']:
            item_to_edit.category_id = request.form['category_id']
        session.add(item_to_edit)
        session.commit()
        return redirect(url_for('displayeverything'))
    else:
        return render_template('edititem.html', item_to_edit=item_to_edit)


@app.route('/catalog/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteitem(item_id):
    # This Page deletes an item
    item_to_delete = session.query(Item).filter_by(id=item_id).one_or_none()
    if item_to_delete.user_id != login_session['user_id']:
        return redirect(url_for('displayeverything'))
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        return redirect(url_for('displayeverything'))
    else:
        return render_template(
            'deleteitem.html', item_to_delete=item_to_delete)


# JSON API Endpoints

@app.route('/catalog/category/<int:category_id>/JSON')
def itemsincategoryJSON(category_id):
    """JSON Endpoint that shows all items in one category """
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


@app.route('/catalog/item/<int:item_id>/JSON')
def itemJSON(item_id):
    """JSON Endpoint that information for one specific item"""
    item = session.query(Item).filter_by(id=item_id).one_or_none()
    return jsonify(item=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
