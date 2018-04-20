from flask import Flask, jsonify, abort, request, make_response
import re
import requests
import json

app = Flask(__name__)

available_ids = list()

shopping_lists = [
    {
        'id': 0,
        'name': 'Pirmadienis',
        'done': False,
        'cart': 'Pienas, Sausainiai',
        'tv_programs': [
            {
                'id': 1,
                'url': 'http://tv_programs:5000/tv_programs/1'
            },
            {
                'id': 2,
                'url': 'http://tv_programs:5000/tv_programs/2'
            }
        ]
    },
    {
        'id': 1,
        'name': 'Pirmadienis',
        'done': True,
        'cart': 'Alus, Medus',
        'tv_programs': [
            {
                'id': 3,
                'url': 'http://tv_programs:5000/tv_programs/3'
            },
            {
                'id': 4,
                'url': 'http://tv_programs:5000/tv_programs/4'
            }
        ]
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

    if 'tv_programs' not in data:
        abort(400, "Missing attribute: tv_programs")         

    if not isinstance(data['cart'], str):
        abort(400, "Expected type of str for 'cart', got: {}".format(type(data['cart'])))

    if not isinstance(data['done'], bool):
        abort(400, "Expected type of bool for 'done', got: {}".format(type(data['done'])))

    if not isinstance(data['tv_programs'], list):
        abort(400, "Expected type of list for 'tv_programs', got: {}".format(type(data['tv_programs'])))    

    new_id = None
    try:
        new_id = available_ids.pop(0)
    except IndexError:
        new_id = len(shopping_lists)

    tv_programs = list()

    try:
        for item in data['tv_programs']:
            check_if_valid_link(item['url'])
            tv_id = int(re.search(r'\/(\d+)', item['url']).group(1))
            tv_programs.append({'url': item['url'], 'id': tv_id})
    except:
        abort(400, "Invalid attribute: tv_programs")

    new_shopping_list = {
        'id': new_id,
        'name': data['name'],
        'done': data['done'],
        'cart': data['cart'],
        'tv_programs': tv_programs
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

    if 'name' not in data or 'cart' not in data or 'done' not in data or 'tv_programs' not in data:
        abort(400, "Attributes 'name', 'done', 'cart' or 'tv_programs' not found")

    if not isinstance(data['cart'], str):
        abort(400, "Expected type of str for 'cart', got: {}".format(type(data['cart'])))

    if not isinstance(data['done'], bool):
        abort(400, "Expected tpye of bool for 'done', got: {}".format(type(data['done'])))

    if not isinstance(data['tv_programs'], list):
        abort(400, "Expected type of list for 'tv_programs', got: {}".format(type(data['tv_programs'])))    

    tv_programs = list()

    try:
        for item in data['tv_programs']:
            check_if_valid_link(item['url'])
            tv_id = int(re.search(r'\/(\d+)', item['url']).group(1))
            tv_programs.append({'url': item['url'], 'id': tv_id})
    except:
        abort(400, "Invalid attribute: tv_programs")


    shopping_lists[index]['name'] = data['name']
    shopping_lists[index]['cart'] = data['cart']
    shopping_lists[index]['done'] = data['done']
    shopping_lists[index]['tv_programs'] = tv_programs

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

    if 'tv_programs' in data:
        shopping_lists[index]['tv_programs'] = data['tv_programs']

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



# ------------- 2 uzduotis ----------------

def check_if_valid_link(link):
    my_request = requests.get(link)
    if my_request.status_code != 200:
        abort(400, "Invalid link. Does not exsist: {}".format(link))


@app.route('/tv_programs', methods=['GET'])
def get_all_tv_programs():
    link = 'http://tv_programs:5000/tv_programs'
    my_request = requests.get(link)
    data = my_request.json()
    return jsonify({'programs': data}), 200

# GET tv programs for shopping list
@app.route('/lists/<int:list_id>/tv_programs', methods=['GET'])
def get_tv_programs(list_id):
    index = get_shopping_list_id_or_abort(list_id)
    tv_list = list()
    for item in shopping_lists[index]['tv_programs']:
        my_req = requests.get(item['url'])
        if my_req.status_code == 404:
            abort(404, "TV program not found")
        data = my_req.json()
        tv_list.append(data)

    return jsonify({'programs': tv_list}), 200


# POST
@app.route('/lists/<int:list_id>/tv_programs', methods=['POST'])
def add_new_tv_program(list_id):
    index = get_shopping_list_id_or_abort(list_id)
    data = request.get_json(force=True)

    new_tv = dict()
    try:
        new_tv['television'] = data['television']
        new_tv['type'] = data['type']
        new_tv['title'] = data['title']
        new_tv['start_time'] = data['start_time']
        new_tv['description'] = data['description']
        new_tv['release_year'] = data['release_year']
        new_tv['legal_age'] = data['legal_age']
    except KeyError:
        abort(400, "Not all attributes provided")

    link = 'http://tv_programs:5000/tv_programs'

    my_req = requests.post(link, json=new_tv)
    
    new_id = int(re.search(r'\/(\d+)',my_req.headers['location']).group(1))


    # new_id = shopping_lists[index]['tv_programs'][-1]['id'] + 1

    shopping_lists[index]['tv_programs'].append({'id': new_id, 'url': my_req.headers['location']})

    resp = make_response("Successfully added")
    resp.headers['location'] = my_req.headers['location']

    resp.headers['symbolic link'] = '/lists/{}/tv_programs/{}'.format(list_id, new_id)
    resp.status_code = 201
    
    return resp

# GET get tv program by id in tv_programas
@app.route('/lists/<int:list_id>/tv_programs/<int:program_id>', methods=['GET'])
def return_tv_program_by_id(list_id, program_id):
    index = get_shopping_list_id_or_abort(list_id)

    for item in shopping_lists[index]['tv_programs']:
        if item['id'] == program_id:
            my_req = requests.get(item['url'])
            if my_req.status_code == 404:
                abort(404, "TV program not found")
            data = my_req.json()

            return jsonify({'tv_program': data}), 200

    abort(404, "TV program with id {} not found".format(program_id))


# DELETE tv program by id
@app.route('/lists/<int:list_id>/tv_programs/<int:program_id>', methods=['DELETE'])
def delete_tv_program_by_id(list_id, program_id):
    index = get_shopping_list_id_or_abort(list_id)

    for item in shopping_lists[index]['tv_programs']:
        if item['id'] == program_id:
            my_req = requests.delete(item['url'])
            if my_req.json()['DELETED'] != 'true':
                abort(400, 'Error in tv_programs service side, item can not be deleted')

            program_index = shopping_lists[index]['tv_programs'].index(item)
            del shopping_lists[index]['tv_programs'][program_index]

            resp = make_response('Successfully removed')
            resp.status_code = 200

            return resp

    abort(404, "TV program with id {} not found".format(program_id))


@app.route('/lists/<int:list_id>/tv_programs/<int:program_id>', methods=['PUT'])
def update_tv_program(list_id, program_id):
    index = get_shopping_list_id_or_abort(list_id)
    data = request.get_json(force=True)

    updated_tv = dict()

    try:
        updated_tv['television'] = data['television']
        updated_tv['type'] = data['type']
        updated_tv['title'] = data['title']
        updated_tv['start_time'] = data['start_time']
        updated_tv['description'] = data['description']
        updated_tv['release_year'] = data['release_year']
        updated_tv['legal_age'] = data['legal_age']
    except KeyError:
        abort(400, "Not all attributes provided")


    for item in shopping_lists[index]['tv_programs']:
        if item['id'] == program_id:
            program_index = shopping_lists[index]['tv_programs'].index(item)
            my_req = requests.put(item['url'], json=updated_tv)
            if my_req.status_code != 200:
                abort(400, 'Something went wrong in TV program service')

            resp = make_response("Successfully updated")
            resp.status_code = 200

            return resp

if __name__== "__main__":
    app.run(host="0.0.0.0", port=5000)
