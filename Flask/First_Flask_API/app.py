from flask import Flask, request, jsonify
# DB connection
from config import Config
# Model(Entity)
from Models.models import db
# Controller
from Controllers.user_controller import user_controller

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(user_controller)

@app.get("/")
def home():
    return "Hello world."

if __name__ == "__main__":
    app.run(debug=True)