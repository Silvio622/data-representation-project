# rest_server file 
# Author: Silvio Dunst

from flask import Flask, request, abort,jsonify
from ProductDAO import *


app = Flask(__name__, static_url_path = '',static_folder = 'staticpages')

# Connect to the index site
@app.route('/')
def index():
    
    return "hello"


# Get all the products from the database productdb via the ProductDAO.py file
@app.route('/products', methods=['GET'])
def getAll():

    return jsonify(productdb.getAll()) 


# Find a product by Id  
@app.route('/products/<int:productid>', methods=['GET'])
def findById(productid):
   
    return jsonify(productdb.findbyId(productid)) 

    
# Insert a new product into the database productdb via the ProductDAO.py file
@app.route('/products', methods=['POST'])
def create():
    
    if not request.json:# if the object is not in JSON format then abort and show error code 400
        abort(400)

    product= {
        "productid": request.json["productid"],
        "productname": request.json["productname"],
        "manufacturer": request.json["manufacturer"], 
        "price": request.json["price"], 
        "vendorid": request.json["vendorid"], 
        }

    return jsonify(productdb.create(product)) 


# Update a product in the database productdb via the ProductDAO.py file
@app.route('/products/<int:productid>', methods=['PUT'])
def update(productid):
    foundproduct = productdb.findbyId(productid)# find the product by productid first in the database
    if foundproduct == {} : # if nothing or no product found in the foundproduct list
        return jsonify({}), 404 # return empty dictionary or code 404 means can't find the product by id

    currentproduct = foundproduct # if a product is found move it into currenproduct variable
    if "productname" in request.json:
        currentproduct["productname"] = request.json["productname"]

    if "manufacturer" in request.json:
        currentproduct["manufacturer"] = request.json["manufacturer"]

    if "price" in request.json:
        currentproduct["price"] = request.json["price"]

    if "vendorid" in request.json:
        currentproduct["vendorid"] = request.json["vendorid"]

    productdb.update(currentproduct)

    return jsonify(currentproduct)
   

# Delete a product from the database productdb via the ProductDAO.py file
@app.route('/products/<int:productid>', methods=['DELETE'])
def delete(productid):
    productdb.delete(productid)

    return jsonify({"done":True})

if __name__ == '__main__':
    app.run(debug=True)
   
