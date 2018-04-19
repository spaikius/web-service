from flask import Flask, jsonify, abort, request, make_response
import re

app = Flask(__name__)

available_ids = list()

shopping_lists = [
    {
        'id': 0,
        'name': 'Pirmadienis',
        'done': False,
        'cart': 'Pienas, Sausainiai'
    },
    {
        'id': 1,
        'name': 'Pirmadienis',
        'done': True,
        'cart': 'Alus, Medus'
    }
]

# Greetings
@app.route('/', methods=['GET'])
def greet():
    return jsonify({'message': 'Welcome to my web service'})


# GET shopping lists
@app.route('/lists', methods=['GET'])
def get_shopping_lists():
    return jsonify({'lists': shopping_lists}), 200


# POST add a new shopping list
@app.route('/lists', methods=['POST'])
def add_new_list():
    data = request.get_json(force=True)

    if 'name' not in data:
        abort(400, "Missing attribute: name")

    if 'cart' not in data:
        abort(400, "Missing attribute: cart")

    if 'done' not in data:
        abort(400, "Missing attribute: done")        

    if not isinstance(data['cart'], str):
        abort(400, "Expected type of str for 'cart', got: {}".format(type(data['cart'])))

    if not isinstance(data['done'], bool):
        abort(400, "Expected tpye of bool for 'done', got: {}".format(type(data['done'])))        

    new_id = None
    try:
        new_id = available_ids.pop(0)
    except IndexError:
        new_id = len(shopping_lists)

    new_shopping_list = {
        'id': new_id,
        'name': data['name'],
        'done': data['done'],
        'cart': data['cart']
    }

    shopping_lists.append(new_shopping_list)

    resp = make_response("Successfully added")
    resp.headers['href'] = "/lists/{}".format(new_id)
    resp.status_code = 201

    return resp 


# GET return specific list
@app.route('/lists/<int:list_id>', methods=['GET'])
def return_list(list_id):
    index = get_shopping_list_id_or_abort(list_id)
    return jsonify({'list': shopping_lists[index]}), 200


# PUT update shopping list attributes
@app.route('/lists/<int:list_id>', methods=['PUT'])
def update_shopping_list(list_id):
    index = get_shopping_list_id_or_abort(list_id)
    
    data = request.get_json(force=True)

    if 'name' not in data or 'cart' not in data or 'done' not in data:
        abort(400, "Attributes 'name', 'done' or 'cart' not found")

    if not isinstance(data['cart'], str):
        abort(400, "Expected type of str for 'cart', got: {}".format(type(data['cart'])))

    if not isinstance(data['done'], bool):
        abort(400, "Expected tpye of bool for 'done', got: {}".format(type(data['done'])))        

    shopping_lists[index]['name'] = data['name']
    shopping_lists[index]['cart'] = data['cart']
    shopping_lists[index]['done'] = data['done']

    resp = make_response('Successfully updated')
    resp.status_code = 200

    return resp


# PATCH
@app.route('/lists/<int:list_id>', methods=['PATCH'])
def update_attr(list_id):
    index = get_shopping_list_id_or_abort(list_id)

    data = request.get_json(force=True)

    if 'name' in data:
        shopping_lists[index]['name'] = data['name']

    if 'cart' in data:
        shopping_lists[index]['cart'] = data['cart']

    if 'done' in data:
        shopping_lists[index]['done'] = data['done']

    resp = make_response('Successfully updated')
    resp.status_code = 200

    return resp


# DELETE
@app.route('/lists/<int:list_id>', methods=['DELETE'])
def delete_list(list_id):
    index = get_shopping_list_id_or_abort(list_id)

    del shopping_lists[index]

    resp = make_response('Successfully deleted')
    resp.status_code = 200

    return resp


def get_shopping_list_id_or_abort(id):
    for item in shopping_lists:
        if(item['id'] == id):
            return shopping_lists.index(item)

    abort(404, 'Shopping list with id {} does not exist'.format(id))


# Error handler
@app.errorhandler(404)
def not_found(error):
    err_msg = {'error': 'Not found'}
    return make_response(jsonify(err_msg), 404)


if __name__== "__main__":
    app.run(host="0.0.0.0")
