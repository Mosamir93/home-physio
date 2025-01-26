from flask import Blueprint, render_template

general_bp = Blueprint('general', __name__)

@general_bp.route('/', methods=['GET'], strict_slashes=False)
def home():
    return render_template('home.html')
