from flask import Blueprint

product_category_api_blueprint = Blueprint('product_category_api',
                             __name__,
                             template_folder='templates')

@product_category_api_blueprint.route('/', methods=['GET'])
def index():
    return "Product Category API"
