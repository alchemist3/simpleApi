#!/usr/bin/python3
import httplib2
import json
import hashlib

server_url = 'http://127.0.0.1:5000'


def sign_in(login, password):
    url = server_url + '/signIn'
    http = httplib2.Http('.cache')
    hash_object = hashlib.sha256(str.encode(password))
    content = http.request(url, method='GET',
                           headers={'login': login, 'password': hash_object.hexdigest()})[1]
    return json.loads(content.decode('utf-8'))


def get_stock_data(token):
    url = server_url + '/stock'
    http = httplib2.Http('.cache')
    content = http.request(url, method='GET', headers={'token': token})[1]
    return json.loads(content.decode('utf-8'))


# def get_orders_data():
#     url = server_url + '/orders'
#     http = httplib2.Http()
#     content = http.request(url, method='GET')[1]
#     return json.loads(content.decode('utf-8'))


def place_order(order, token):
    url = server_url + '/orders'
    http = httplib2.Http()
    content = http.request(url, method='POST', body=json.dumps(order),
                           headers={'Content-type': 'application/json; charset=UTF-8', 'token': token})[1]
    return json.loads(content.decode('utf-8'))
