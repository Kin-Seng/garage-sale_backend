from app import app
import garage_sale_api
import garage_sale_web

from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    # app.run()
    cors.run()
