from flask import Flask, jsonify, abort, request, make_response
import re

app = Flask(__name__)

available_ids = list()

shopping_list = [
    {
        'id': 0,
        'name': 'Pirmadienis',
        'done': False,
        'list': [
            {
                'product_id': 0,
                'product': 'Pienas',
                'quantity': 1
            },
            {
                'product_id': 1,
                'product': 'Agurku',
                'quantity': 5
            }
        ]
    },
    {
        'id': 1,
        'name': 'Antradienis',
        'done': False,
        'list': [
            {
                'product_id': 0,
                'product': 'Kefyro',
                'quantity': 2
            },
            {
                'product_id': 1,
                'product': 'Sausainiu',
                'quantity': 3
            }
        ]
    },
]

def get_index_or_abort(list_id, product_id=None):
    counter = 0
    for lst in shopping_list:
        if lst['id'] == list_id:
            if product_id is None:
                return counter
            else:
                p_counter = 0
                for item in lst['list']:
                    if item['product_id'] == product_id:
                        return counter, p_counter

                    p_counter += 1

        counter += 1

    abort(404, 'Shopping list with id {} does not exist'.format(list_id))


# Return all shopping lists or by name
@app.route('/lists', methods=['GET'])
def get_shopping_lists():
    if request.args.get('name', None):
        found_list = list()
        for lst in shopping_list:
            if re.search(request.args.get('name', None), lst["name"], re.I):
                found_list.append(lst)
        return jsonify(found_list), 200
    else:
        return jsonify(shopping_list), 200


# Add a new shopping list
@app.route('/lists', methods=['POST'])
def create_shopping_list():
    data = request.get_json(force=True)

    try:
        name = data['name']
        done = data['done']
    except:
        abort(400, "name or status 'done' not found. Got {}".format(data))

    if not isinstance(done, bool):
        abort(400, "Status 'done' is not type of boolean")

    try:
        lst = data['list']

        id_count = 0
        for item in lst:
            
            item['product_id'] = id_count
            id_count += 1

    except:
        lst = [{'product_id': 0, 'product': None, 'quantity': None}]

    new_id = None

    try:
        new_id = available_ids.pop(0)
    except IndexError:
        new_id = len(shopping_list)

    new_shopping_list = {
        'id': new_id,
        'name': name,
        'done': done,
        'list': lst
    }

    shopping_list.append(new_shopping_list)

    resp = make_response('Gut')
    resp.headers['URL'] = 'https://kazkur.com'
    

    return jsonify(new_shopping_list), 201, resp 


# Return shopping list by id
@app.route('/lists/<int:list_id>', methods=['GET'])
def get_list(list_id):
    index = get_index_or_abort(list_id)

    return jsonify(shopping_list[index])

@app.route('/lists/<int:list_id>/products', methods=['GET'])
def get_products_list(list_id):
    index = get_index_or_abort(list_id)

    return jsonify(shopping_list[index]['list'])


@app.route('/lists/<int:list_id>', methods=['PATCH'])
def list_patch(list_id):
    index = get_index_or_abort(list_id)
    data = request.get_json(force=True)

    

# Change shopping list attributes by id
@app.route('/lists/<int:list_id>', methods=['PUT'])
def change_info(list_id):
    index = get_index_or_abort(list_id)

    data = request.get_json(force=True)

    name = None
    done = None
    lst = None

    try:
        name = data['name']
    except KeyError:
        abort(400, "Missing attribute 'name'")

    try:
        done = data['done']
    except KeyError:
        abort(400, "Missing attribute 'done'")

    if not isinstance(done, bool) and done is not None:
        abort(400, "Status 'done' is not type of boolean")

    try:
        lst = data['list']
    except KeyError:
        abort(400, "Missing attribute 'done'")

    if lst:
        if not isinstance(lst, list):
            abort(400, 'Expected list, got {}'.format(lst))

        for item in lst:
            if not isinstance(item, dict):
                abort(400, 'Expected dictionary, got {}'.format(item))

        shopping_list[index]['list'] = lst

    if done:
        shopping_list[index]['done'] = done

    if name:
        shopping_list[index]['name'] = name

    return jsonify(shopping_list[index]), 200


@app.route('/lists/<int:list_id>', methods=['POST'])
def add_new_product(list_id):
    l_index = get_index_or_abort(list_id)
    data = request.get_json(force=True)

    new_id = 0

    ids = [_id['product_id'] for _id in shopping_list[l_index]['list']]

    while new_id in ids:
        new_id += 1

    try:
        new_product = {
            'product_id': new_id,
            'product': data['product'],
            'quantity': data['quantity']
        }
    except:
        abort(400, 'Product or its quantity not found')

    shopping_list[l_index]['list'].append(new_product)

    return jsonify(new_product), 200


# Delete shopping list by id
@app.route('/lists/<int:list_id>', methods=['DELETE'])
def delete_shopping_list(list_id):
    index = get_index_or_abort(list_id)

    del shopping_list[index]

    available_ids.append(index)
    
    return jsonify(True), 200


@app.route('/lists/<int:list_id>/products/<int:product_id>', methods=['GET'])
def get_product(list_id, product_id):
    l_index, p_index = get_index_or_abort(list_id, product_id)
    return jsonify(shopping_list[l_index]['list'][p_index]), 200


@app.route('/lists/<int:list_id>/products/<int:product_id>', methods=['PUT'])
def update_product(list_id, product_id):
    l_index, p_index = get_index_or_abort(list_id, product_id)
    data = request.get_json(force=True)

    product = None
    quantity = None

    try:
        product = data['product']
    except:
        pass

    try:
        quantity = data['quantity']
        quantity += 0
    except TypeError:
        abort(400, 'Expected integer got {}'.format(data['quantity']))
    except:
        pass

    if product:
        shopping_list[l_index]['list'][p_index]['product'] = product
    if quantity:
        shopping_list[l_index]['list'][p_index]['quantity'] = quantity

    return jsonify(shopping_list[l_index]['list'][p_index]), 200


@app.route('/lists/<int:list_id>/products/<int:product_id>', methods=['DELETE'])
def delete_product(list_id, product_id):
    l_index, p_index = get_index_or_abort(list_id, product_id)
    del shopping_list[l_index]['list'][p_index]
    return jsonify(True), 200


# Error handler
@app.errorhandler(404)
def not_found(error):
    err_msg = {'error': 'Not found'}
    return make_response(jsonify(err_msg), 404)


if __name__== "__main__":
    app.run(host="0.0.0.0")