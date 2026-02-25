import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/base', methods=['GET', 'POST'])
def base():
    return render_template('auth/base.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html')