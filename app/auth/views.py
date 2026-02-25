import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from .forms import (
    LoginForm, 
    RegistrationForm
)
from app.models.users import User

auth = Blueprint('auth', __name__)


@auth.route('/base', methods=['GET', 'POST'])
def base():
    return render_template('auth/base.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.get_user_by_email(form.email.data)

        if user is None:
            flash('Email ou mot de passe incorrects.')
            return redirect(url_for('auth.login'))

        if not user.is_actived:
            flash('Votre compte n\'est pas activé.')
            return redirect(url_for('auth.login'))

        if user is not None and user.verify_password(form.password.data) and user.is_actived:
            login_user(user) #form.remember_me.data
            next = request.args.get('next')

            if next is None or not next.startswith('/'):
                next = url_for('main.dashboard')
            return redirect(next)
        
        # reinitialise state
        form.email.data = ''
        form.remember_me.data = False
        flash('Email ou mot de passe incorrects.')

    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # firstname = form.firstname.data or ''
        # lastname = form.lastname.data or ''
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Validation
        user = User.get_user_by_email(email)
        print("Utilisateur trouvé : ", user)
        
        if user:
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return redirect(url_for('auth.register'))

        # # password validation
        # if len(password) < 8:
        #     flash('Le mot de passe doit contenir au moins 8 caractères.', 'danger')
        #     return redirect(url_for('auth.register'))
        # if not re.search(r"[A-Z]", password):
        #     flash('Le mot de passe doit contenir au moins une lettre majuscule.', 'danger')
        #     return redirect(url_for('auth.register'))
        # if not re.search(r"[a-z]", password):
        #     flash('Le mot de passe doit contenir au moins une lettre minuscule.', 'danger')
        #     return redirect(url_for('auth.register'))
        # if not re.search(r"[0-9]", password):
        #     flash('Le mot de passe doit contenir au moins un chiffre.', 'danger')
        #     return redirect(url_for('auth.register'))
        # if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?£`>~])[A-Za-z\d!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?£`>~]{8,}$', password):
        #     flash('Le mot de passe doit contenir au moins un caractère spécial.', 'danger')
        #     return redirect(url_for('auth.register'))

        # Create new user
        new_user = User(
            email=email,
            password=password,
        )

        print("Nouvel utilisateur créé : ", new_user)

        new_user.save()
        return redirect(url_for('auth.login'))  

    return render_template('auth/register.html', form=form)