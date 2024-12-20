from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
from flask_cors import CORS
from werkzeug.utils import secure_filename
from base import db
from user import User
import os


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the database credentials from environment variables
user = os.getenv("DB_USER", "root")
pin = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "mediamatch_db")

# Configuring database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and CORS
db.init_app(app)
CORS(app)

# Create database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    name = data.get('name')
    age = data.get('age')
    movies = data.get('movies', [])
    games = data.get('games', [])

    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400

    new_user = User(name=name, age=age, movies=movies, games=games)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
