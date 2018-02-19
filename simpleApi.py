#!/usr/bin/python3
from flask import Flask, jsonify, request, abort, make_response
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import config

app = Flask(__name__)

users = [
    {
        'user_id': 1,
        'login': 'testUser',
        'hashed_password': 'test'
    },
    {
        'user_id': 2,
        'login': 'someUser1',
        'hashed_password': 'test'
    }
]

stock = [
    {
        'stock_id': 1,
        'product': 'hammer',
        'amount': 1000
    },
    {
        'stock_id': 2,
        'product': 'chainsaw',
        'amount': 50
    },
    {
        'stock_id': 3,
        'product': 'screwdriver',
        'amount': 100
    }
]

orders = []


def generate_token(user_id, expiration=config.token_expiration):
    s = Serializer(config.secret_key, expires_in=expiration)
    return s.dumps({'user_id': user_id})


def verify_token(token):
    s = Serializer(config.secret_key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False  # expired token
    except BadSignature:
        return False  # invalid token
    return data['user_id']


@app.route('/signIn', methods=['POST'])
def sign_in():
    if not request.json:
        abort(400)

    login = request.json['login']
    password = request.json['password']

    dict_index = next((index for (index, d) in enumerate(users) if d['login'] == login), None)
    if dict_index is not None:
        if users[dict_index]['hashed_password'] == password:
            token = generate_token(users[dict_index]['user_id'])
            return token
        else:
            abort(401)
    else:
        abort(400)


@app.route('/stock', methods=['GET'])
def get_stock():
    token = request.headers['token']
    if verify_token(token):
        return jsonify({'stock': stock})
    else:
        abort(401)


# @app.route('/orders', methods=['GET'])
# def get_orders():
#     return jsonify({'orders': orders})


@app.route('/orders', methods=['POST'])
def place_order():
    token = request.headers['token']
    user_id = verify_token(token)
    if user_id:
        if not request.json:
            abort(400)

        if len(orders) > 0:
            order_id = orders[-1]['order_id'] + 1
        else:
            order_id = 1

        stock_id = request.json['stock_id']
        amount = request.json['amount']

        dict_index = next((index for (index, d) in enumerate(stock) if d['stock_id'] == stock_id), None)

        if dict_index is not None and amount <= stock[dict_index]['amount']:
            stock[dict_index]['amount'] -= amount

            order = {
                'order_id': order_id,
                'stock_id': stock_id,
                'buyer_id': user_id,
                'amount': amount
            }

            orders.append(order)
            return jsonify({'order': order}), 201
        else:
            abort(400)
    else:
        abort(401)


# 401 Unauthorized
@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized'}), 401)


# 400 Bad request
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    app.run()
