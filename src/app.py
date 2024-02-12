"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Generate a new member
@app.route('/member', methods=['POST'])
def add_member():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    member = request.get_json()
    if 'first_name' not in member or 'age' not in member or 'lucky_numbers' not in member:
        return jsonify({"msg": "All parameters are required"}), 400
    
    jackson_family.add_member(member)
    return jsonify({"msg": "Member added successfully"}), 200

# Get all members
@app.route('/members', methods=['GET'])
def handle_hello():
    try:
    # this is how you can use the Family datastructure by calling its methods
        members = jackson_family.get_all_members()
        response = jsonify(members)
        response.headers.set('Content-Type', 'application/json')
    # response_body = {
    #     "hello": "world",
    #     "family": members
    # }
        if not members:
          return jsonify({"msg": "No members found"}), 400
        return jsonify(members), 200
    except Exception as e:
       return jsonify({"msg": "An error ocurred"}), 500
    
# Get one member
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"msg": "Member not found"}), 400
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"msg": "An error ocurred" + str(e)}), 500
    
# Delete one member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        try:
            jackson_family.delete_member(member_id)
            return jsonify({"msg": "Member deleted successfully"}), 200
        except Exception as e:
            return jsonify({"msg": "An error ocurred" + str(e)}), 500
    else:
        return jsonify({"msg": "Member not found"}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
