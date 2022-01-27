from flask import Flask, jsonify, request, render_template


app = Flask(__name__)
stores = [
    {
        'name': 'My worderfull store',
        'items': [
            {
            'name': 'My Item',
            'price': 15.99
            }       
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

# POST - Receive data
# GET - Send data back

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over stores, if the store name matches, return it, if none match, return an error.
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, pri    ce:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'items': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not store'})
    

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_store(name):
     # Iterate over stores
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)