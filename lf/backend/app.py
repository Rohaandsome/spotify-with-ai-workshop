from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, request
from flask_cors import CORS

from services.routes import routes
app = Flask(__name__)
app.register_blueprint(routes)

CORS(app)

if __name__ == "__main__":
  app.run(debug=True)