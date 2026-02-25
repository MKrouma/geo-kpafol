import os
from flask import (
    render_template, Blueprint, jsonify, redirect, 
    url_for, send_from_directory, current_app, request
)
from flask_login import login_required, current_user

main = Blueprint('main', __name__, 
                static_folder='static',  # Add static folder
                template_folder='templates'  # Add template folder
)



# FRONTEND 
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html') 