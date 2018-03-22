""" Description:
    Restful web-service: shopping list

    file name: api.py

    Author: Rimvydas Noreika
    Date: 2018-03-16
"""

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

parser.add_argument('buy')
parser.add_argument('done')
parser.add_argument('id')

# keeps a track of removed ids
avialable_ids = list()

# Sample
shopping_list = [
    {
        'id': 0,
        'done': False,
        'buy': ['Duonos', 'Pieno', 'Kavos', 'Arbatos']
    },
    {
        'id': 1,
        'done': False,
        'buy': ['Pieno', 'Medaus', 'Kakavos']
    },
    {
        'id': 2,
        'done': True,
        'buy': ['Kefyro', 'Saldainių']
    },
]


def get_position_or_abort(list_id):
    """ Loop through shopping_list and return index if list id match
        given id. Abort if no match found
    """
    try:
        list_id = int(list_id)
    except:
        abort(400, message="Bad list id: {}".format(list_id))

    for i in range(0, len(shopping_list)):
        if shopping_list[i]['id'] == list_id:
            return i

    abort(404, message="List id: {} doesn't exist".format(list_id))


def abort_if_no_exist(list_id, product_id):
    """ Check if product id exist if no abort else retrun id(int) """
    try:
        product_id = int(product_id)
    except:
        abort(400, message="Bad product id: {}".format(product_id))
       
    if product_id < 0:
        abort(400, message="Bad product id: {}".format(product_id)) 

    if product_id > len(shopping_list[list_id]['buy']) - 1:
        abort(404, message="Product id: {} doesn't exist".format(product_id))
    
    return product_id
        

class ShoppingList(Resource):
    """ Root of shopping_list
        Avialable methods:
            GET: return all shopping lists
            POST: add a new shopping list
            DELETE: remove shopping list by id
    """
    def get(self):
        return shopping_list

    def post(self):
        args = parser.parse_args()
        list_id = None
        try:
           list_id = avialable_ids.pop(0)
        except IndexError:
            list_id = len(shopping_list)

        buy_list = None

        if args['buy']:
            try:
                buy_list = json.loads(args['buy'])
            except:
                abort(400)
            
            if not isinstance(buy_list, list):
                abort(400, message="Expected list, got {}".format(args['buy']))
        else:
            buy_list = list()


        new_shopping_list = {
            'id': list_id,
            'done': False,
            'buy': buy_list
        }

        shopping_list.append(new_shopping_list)

        return new_shopping_list, 201


    def delete(self):
        args = parser.parse_args()
        
        index = get_position_or_abort(args['id'])
        
        del shopping_list[index]

        avialable_ids.append(index)
        
        return '', 204


class Shopping(Resource):
    """ Inner child of shopping_list 
        Avialable methods:
            GET: Return inner child of shopping_list
            PUT: Update attribute 'done'
            POST: Append new 'list item' to attribute 'buy'
    """
    def get(self, list_id):
        index = get_position_or_abort(list_id)
        return shopping_list[index]

    def put(self, list_id):
        args = parser.parse_args()
        index = get_position_or_abort(list_id)
        
        try:
            if args['done'] in ['True', 'true']:
                shopping_list[index]['done'] = True
            elif args['done'] in ['False', 'false']:
                shopping_list[index]['done'] = False
            else:
                abort(400)
        except:
            abort(400)

        return shopping_list[index], 201

    def post(self, list_id):
        args = parser.parse_args()
        
        index = get_position_or_abort(list_id)
        
        shopping_list[index]['buy'].append(args['buy'])
        
        return shopping_list[index]['buy'], 201


class Product(Resource):
    """ Inner childs attribute 'buy' of shopping_list  
        Avialable methods:
            GET: get product by product_id (list index)
            PUT: update product by product_id (list index)
            DELETE: delete product from list by product_id (list index)
    """
    def get(self, list_id, product_id):

        index = get_position_or_abort(list_id)
        product_id = abort_if_no_exist(index, product_id)

        return shopping_list[index]['buy'][product_id]

    def put(self, list_id, product_id):
        args = parser.parse_args()

        index = get_position_or_abort(list_id)
        product_id = abort_if_no_exist(index, product_id)

        shopping_list[index]['buy'][product_id] = args['buy']
        
        return shopping_list[index]['buy'][product_id], 201

    def delete(self, list_id, product_id):
        index = get_position_or_abort(list_id)
        product_id = abort_if_no_exist(index, product_id)

        del shopping_list[index]['buy'][product_id]

        return shopping_list[index]['buy'][product_id], 204


## routing
api.add_resource(ShoppingList, '/')
api.add_resource(Shopping, '/<list_id>')
api.add_resource(Product, '/<list_id>/<product_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
