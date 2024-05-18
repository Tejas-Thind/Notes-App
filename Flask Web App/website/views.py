from flask import Blueprint

views = Blueprint('views', __name__)

# decorator
@views.route('/')
def home():
    return "<h1>Test</h1>"