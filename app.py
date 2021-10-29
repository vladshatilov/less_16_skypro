# -*- coding:utf-8 -*-
import json

from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

# from tables.table_def import User, Offer, Order
# from tables.table_def import fill_db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://127.0.0.1:5000/test.db'
# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Q:/react_apps/flask/flaskProject_lesson16/test.db'
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self):
        return {"id": self.id, "first_name": self.first_name, "last_name": self.last_name, "age": self.age,
                "email": self.email, "role": self.role, "phone": self.phone}


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)

    def to_dict(self):
        return {"id": self.id, "order_id": self.order_id, "executor_id": self.executor_id}


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String(255))
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": u"{0}".format(self.description),
                "start_date": self.start_date, "end_date": self.end_date, "address": self.address, "price": self.price,
                "customer_id": self.customer_id, "executor_id": self.executor_id}


def fill_db(class_name, json_file):
    with open(json_file, 'r', encoding='utf-8') as users_js:
        users_dict = json.load(users_js)
        for i in range(len(users_dict)):
            john = class_name(**users_dict[i])
            db.session.add(john)
            del john
        db.session.commit()


db.drop_all()
db.create_all()

fill_db(User, 'users.json')
fill_db(Order, 'orders.json')
fill_db(Offer, 'offers.json')


@app.route('/')
def hello_world():
    return render_template('home.html')


# **Шаг 3**
# Создайте представление для пользователей, которое обрабатывало бы `GET`-запросы получения всех пользователей `/users`
# Шаг 6
# Реализуйте создание пользователя user посредством метода POST на URL /users  для users.
@app.route('/users', methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        res = User.query.all()
        temp_t = []
        for i in res:
            temp_t.append(i.to_dict())
        return jsonify(temp_t)
    elif request.method == 'POST':
        db.session.add(User(**request.form.to_dict()))
        db.session.commit()
        return redirect('http://127.0.0.1:5000/users',code=200)

# **Шаг 3**
# Создайте представление для пользователей, которое обрабатывало бы `GET`-запросы пользователя по идентификатору `/users/1`.
# **Шаг 6**
# Реализуйте обновление пользователя `user` посредством метода PUT на URL `/users/<id>`  для users. В Body будет приходить JSON со всеми полями для обновление заказа.
# Реализуйте удаление пользователя `user` посредством метода DELETE на URL `/users/<id>` для users.
@app.route('/users/<int:uid>',methods=['GET','POST'])
def get_one_user(uid):
    if request.method == 'GET':
        res = User.query.get(uid)
        return jsonify(res.to_dict())
    elif request.method == 'POST':
        if request.form.get('_method')=='put':
            user_to_change = User.query.get(request.form['id'])
            user_to_change.id = request.form.get('id')
            user_to_change.first_name = request.form.get('first_name')
            user_to_change.last_name = request.form.get('last_name')
            user_to_change.age = request.form.get('age')
            user_to_change.email = request.form.get('email')
            user_to_change.role = request.form.get('role')
            user_to_change.phone = request.form.get('phone')
            db.session.add(user_to_change)
            db.session.commit()
            return redirect('http://127.0.0.1:5000/users', code=200)
        elif request.form.get('_method')=='delete':
            User.query.filter(User.id == request.form.get('id')).delete()
            db.session.commit()
            return redirect('http://127.0.0.1:5000/users', code=200)
        return 'error'


# **Шаг 4**
# Создайте представление для заказов, которое обрабатывало бы `GET`-запросы получения всех заказов `/orders` и заказа по идентификатору `/orders/1`.
@app.route('/orders')
def get_all_orders():
    res = Order.query.all()
    temp_t = []
    for i in res:
        temp_t.append(i.to_dict())
    return jsonify(temp_t)

# **Шаг 4**
@app.route('/orders/<int:uid>')
def get_one_order(uid):
    res = Order.query.get(uid)
    # return json.dumps(res.to_dict())
    return jsonify(res.to_dict())


# **Шаг 5**
# Создайте представление для предложений, которое обрабатывало бы `GET`-запросы получения всех предложений `/offers` и предложения по идентификатору `/offers/<id>`.
@app.route('/offers')
def get_all_offers():
    res = Offer.query.all()
    temp_t = []
    for i in res:
        temp_t.append(i.to_dict())
    return jsonify(temp_t)

# **Шаг 5**
@app.route('/offers/<int:uid>')
def get_one_offer(uid):
    res = Offer.query.get(uid)
    return jsonify(res.to_dict())


if __name__ == '__main__':
    app.run()
