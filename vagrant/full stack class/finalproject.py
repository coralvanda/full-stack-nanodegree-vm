from flask import Flask, render_template, url_for
from flask import request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurant/')
@app.route('/restaurants')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants =
		restaurants)


@app.route('/restaurant/new', methods =	['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		new_rest = Restaurant(name = request.form['name'])
		session.add(new_rest)
		session.commit()
		flash("New restaurant added!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods =
	['GET', 'POST'])
def editRestaurant(restaurant_id):
	rest_to_edit = session.query(Restaurant).filter_by(id =
		restaurant_id).one()
	if request.method == 'POST':
		rest_to_edit.name = request.form['name']
		session.add(rest_to_edit)
		session.commit()
		flash("Restaurant name changed!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant =
		rest_to_edit)


@app.route('/restaurant/<int:restaurant_id>/delete', methods =
	['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	rest_to_del = session.query(Restaurant).filter_by(id =
		restaurant_id).one()
	if request.method == 'POST':
		session.delete(rest_to_del)
		session.commit()
		flash("Restaurant removed!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant =
		rest_to_del)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id =
		restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id =
		restaurant_id).all()
	return render_template('menu.html', restaurant =
		restaurant, items = items)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods =
	['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id =
		restaurant_id).one()
	if request.method == 'POST':
		new_item = MenuItem(name = request.form['name'], 
			description = request.form['desc'],
			price = request.form['price'],
			restaurant_id = restaurant_id)
		session.add(new_item)
		session.commit()
		return redirect(url_for("showMenu", restaurant_id =
			restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant =
		restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', 
	methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		item.name = request.form['name']
		item.description = request.form['desc']
		item.price = request.form['price']
		session.add(item)
		session.commit()
		flash("Menu item name changed!")
		return redirect(url_for('showMenu', restaurant_id = 
			restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id =
		restaurant_id, item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', 
	methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash("Menu item deleted!")
		return redirect(url_for('showMenu', restaurant_id =
			restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant_id = 
		restaurant_id, item = item)





if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)