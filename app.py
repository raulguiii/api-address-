from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addresses.db'

db = SQLAlchemy(app)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))

    def __repr__(self):
        return f'<Address {self.id}>'

@app.route('/address', methods=['POST'])
def create_address():
    data = request.get_json()
    new_address = Address(street=data['street'], city=data['city'], state=data['state'], postal_code=data['postal_code'])
    db.session.add(new_address)
    db.session.commit()
    return jsonify({'message': 'Address created successfully'}), 201

@app.route('/address', methods=['GET'])
def get_addresses():
    addresses = Address.query.all()
    return jsonify([{'id': address.id, 'street': address.street, 'city': address.city, 'state': address.state, 'postal_code': address.postal_code} for address in addresses])

@app.route('/address/<int:id>', methods=['PUT'])
def update_address(id):
    address = Address.query.get(id)
    if not address:
        return jsonify({'message': 'Address not found'}), 404
    data = request.get_json()
    address.street = data.get('street', address.street)
    address.city = data.get('city', address.city)
    address.state = data.get('state', address.state)
    address.postal_code = data.get('postal_code', address.postal_code)
    db.session.commit()
    return jsonify({'message': 'Address updated successfully'})

@app.route('/address/<int:id>', methods=['DELETE'])
def delete_address(id):
    address = Address.query.get(id)
    if not address:
        return jsonify({'message': 'Address not found'}), 404
    db.session.delete(address)
    db.session.commit()
    return jsonify({'message': 'Address deleted successfully'})

@app.route('/address/from/<int:id>', methods=['GET'])
def get_addresses_from_id(id):
    addresses = Address.query.filter(Address.id == id).all()
    if not addresses:
        return jsonify({'message': 'No addresses found'}), 404
    return jsonify([{
        'id': address.id,
        'street': address.street,
        'city': address.city,
        'state': address.state,
        'postal_code': address.postal_code
    } for address in addresses])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
