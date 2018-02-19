import pprint
from simpleApiClient import sign_in, get_stock_data, place_order

# signing up and getting token
print('\nSigning up with valid user credentials and getting token:')
token = sign_in('testUser', 'test')
print(token)

# trying to log to nonexisting user account
print('\nTrying to log to nonexisting user account:')
token2 = sign_in('test1212', 'asdasdasd')
print(token2)

# trying to log to existing user account with wrong password
print('\nTrying to log to existing user account with wrong password:')
token3 = sign_in('testUser', 'asdasdasd')
print(token3)

# getting stock info with valid token
print('\nGetting stock info with valid token:')
stock = get_stock_data(token['token'])
pprint.pprint(stock)

# trying to get stock info with invalid token
print('\nTrying to get stock info with invalid token:')
stock = get_stock_data('asdasdsadsad464asd684as68d4')
pprint.pprint(stock)


# placing sample order with valid token
print('\nPlacing sample order with valid token:')
sample_order = {
    'stock_id': 1,
    'amount': 10
}
order = place_order(sample_order, token['token'])
pprint.pprint(order)

# getting stock info
print('\nStock changed after placing order:')
stock = get_stock_data(token['token'])
pprint.pprint(stock)

# trying to place an sample order with invalid token
print('\nTrying to place an sample order with invalid token:')
order = place_order(sample_order, 'asdsadasdasdsad')
pprint.pprint(order)

# trying to place an improper sample order with valid token
print('\nTrying to place an improper sample order with valid token:')
sample_order = {
    'asdas': 1,
    'oioj': 10
}
order = place_order(sample_order, token['token'])
pprint.pprint(order)

# trying to place an sample order that exceeds stock state with valid token
print('\nTrying to place an sample order that exceeds stock state with valid token:')
sample_order = {
    'stock_id': 1,
    'amount': 10000
}
order = place_order(sample_order, token['token'])
pprint.pprint(order)

