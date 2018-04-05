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
                'product': 'Pienas',
                'quantity': 1
            },
            {
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
                'product': 'Kefyro',
                'quantity': 2
            },
            {
                'product': 'Sausainiu',
                'quantity': 3
            }
        ]
    },
]


def get_index_or_abort(list_id):
    counter = 0
    for lst in shopping_list:
        if lst['id'] == list_id:
            return counter
        counter += 1

    abort(404, 'Shopping list with id {} does not exist'.format(list_id))


# Return all shopping lists or by name
@app.route('/shopping', methods=['GET'])
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
@app.route('/shopping', methods=['POST'])
def create_shopping_list():
    data = request.get_json(force=True)

    try:
        name = data['name']
        done = data['done']
    except:
        abort(400, "name or status 'done' not found. Got {}".format(data))

    try:
        lst = data['list']

        if not isinstance(lst, list):
            abort(400, 'Expected list, got {}'.format(lst))

        for item in lst:
            if not isinstance(item, dict):
                abort(400, 'Expected dictionart, got {}'.format(item))

    except:
        lst = [{'product': None, 'quantity': None}]

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

    return jsonify(new_shopping_list), 201


# Return shopping list by id
@app.route('/shopping/<int:list_id>', methods=['GET'])
def get_list(list_id):
    index = get_index_or_abort(list_id)

    return jsonify(shopping_list[index])

    
# Change shopping list attributes by id
@app.route('/shopping/<int:list_id>', methods=['PUT'])
def change_info(list_id):
    index = get_index_or_abort(list_id)

    data = request.get_json(force=True)

    name = None
    done = None
    lst = None

    try:
        name = data['name']
        done = data['done']
        lst = data['list']
    except KeyError:
        pass

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


# Delete shopping list by id
@app.route('/shopping/<int:list_id>', methods=['DELETE'])
def delete_shopping_list(list_id):
    index = get_index_or_abort(list_id)

    del shopping_list[index]

    available_ids.append(index)
    
    return jsonify(True), 200


# Error handler
@app.errorhandler(404)
def not_found(error):
    err_msg = {'error': 'Not found'}
    return make_response(jsonify(err_msg), 404)


if __name__== "__main__":
    app.run(host="0.0.0.0", debug=True)