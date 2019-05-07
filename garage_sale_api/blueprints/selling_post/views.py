from flask import Blueprint,jsonify,request
from models.selling_post import SellingPost
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
)

import braintree
import os

selling_post_api_blueprint = Blueprint('selling_post_api',
                             __name__,
                             template_folder='templates')

def transact(options):
    return gateway.transaction.sale(options)

# todo add your own id and keys
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get("BT_MERCHANT_ID"),
        public_key=os.environ.get("BT_PUBLIC_KEY"),
        private_key=os.environ.get("BT_PRIVATE_KEY")
    )
)

@selling_post_api_blueprint.route('/', methods=['GET'])
def index():
    return "Selling Post API"

@selling_post_api_blueprint.route('/market', methods=['GET'])
# @jwt_required
def market():
    marketlist = SellingPost.select().where(SellingPost.buyer.is_null(True))

    return jsonify({
        "status": "success",
        "market": [{
            "product_id": str(market.id),
            "product_name":market.product_name,
            "price": str(market.price),
            "seller_name":str(market.seller.username),
            "pymt_sts":market.pymt_sts
        } for market in marketlist]
    }), 200

@selling_post_api_blueprint.route('/mySellingPost/<id>', methods=['GET'])
@jwt_required
def my_market(id):
    
    myPosts = SellingPost.select().where(SellingPost.seller_id==id)

    return jsonify({
        "status": "success",
        "myPosts": [{
            "product_id": str(myPost.id),
            "product_name":myPost.product_name,
            "price": str(myPost.price),
            "buyer_name": myPost.buyer.username if myPost.buyer else None,
            "pymt_sts":myPost.pymt_sts
        } for myPost in myPosts]
    }), 200


@selling_post_api_blueprint.route('/purchase', methods=['POST'])
# @jwt_required
def purchase():

    #chk if the request is in JSON format
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    product_id = request.json.get('product_id', None)
    buyer = request.json.get('buyer_id', None)

    if product_id and buyer:

        SellingPost.update(buyer_id=buyer,pymt_sts=True).where(SellingPost.id==product_id).execute()

        return jsonify({
            "status": "success",
            "message": "You have successfully purchased this Item"
        }), 200
    else:
        return jsonify({
            "status": "failed",
            "message": "You have issue purchasing this Item"
        }), 404
    



@selling_post_api_blueprint.route('/create', methods=['POST'])
def sp_create():

    #chk if the request is in JSON format
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    product_name = request.json.get('product_name', None)
    price = request.json.get('price', None)
    seller_id = request.json.get('seller_id', None)

    sp = SellingPost(product_name=product_name,price=price,seller_id=seller_id,pymt_sts=False)

    if sp.save():

        return jsonify({
            "status": "success",
            "message": "You have successfully posted this Item for sale"
        }), 200
    else:

        return jsonify({"status": "failed"}), 400

@selling_post_api_blueprint.route('/delete/<product_id>', methods=['POST'])
def sp_delete(product_id):
    
    SellingPost.delete().where(SellingPost.id==product_id).execute()

    if product_id :
        return jsonify({
            "status": "success",
            "message": "You have successfully deleted this post"
        }), 200
    else:
        return jsonify({
            "status": "failed",
            "message": "This Item/Post does not exist in your post list"
        }), 404

    return "Selling Post delete API"


# get Nounce Token
@selling_post_api_blueprint.route('/getToken', methods=['GET'])
@jwt_required
def getToken():
    client_token = gateway.client_token.generate()
    return jsonify(client_token=client_token)


# Payment & update DB
@selling_post_api_blueprint.route('/pay/<product_id>', methods=['POST'])
def pay(product_id):
    # receive nounce from html
    nonce_from_the_client = request.form["payment_nounce"]
    price = str(request.form["price"]) 

    # send to braintree server
    result = transact({
        "amount": price,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
        "submit_for_settlement": True
        }
    })

    if result.is_success:
        SellingPost.update(pymt_sts=True).where(SellingPost.id==product_id).execute()

        return jsonify({
            "status": "success",
            "message": "You have paid for this Item"
        }), 200
    else:
        return jsonify({
            "status": "failed",
            "message": "Payment for your desired item failed"
        }), 400             


