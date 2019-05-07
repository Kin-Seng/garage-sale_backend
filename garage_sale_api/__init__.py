from app import app
# from flask_cors import CORS

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from garage_sale_api.blueprints.users.views import users_api_blueprint
from garage_sale_api.blueprints.product_category.views import product_category_api_blueprint
from garage_sale_api.blueprints.selling_post.views import selling_post_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(product_category_api_blueprint, url_prefix='/api/v1/product_category')
app.register_blueprint(selling_post_api_blueprint, url_prefix='/api/v1/selling_post')