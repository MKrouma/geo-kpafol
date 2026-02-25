import os
from flask import (
    render_template, Blueprint, jsonify, redirect, 
    url_for, send_from_directory, current_app, request
)
from flask_login import login_required, current_user
from app.auth.forms import LoginForm

main = Blueprint('main', __name__, 
                static_folder='static',  # Add static folder
                template_folder='templates'  # Add template folder
)



# FRONTEND 
@main.route('/')
def index():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html', form=form) 

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dash.html')