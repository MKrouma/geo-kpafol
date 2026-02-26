from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models.users import User


class LoginForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[DataRequired(), Length(1, 64), Email()]
    )
    password = PasswordField(
        'Mot de passe',
        validators=[DataRequired()]
    )
    remember_me = BooleanField(
        'Se souvenir de moi',
        default=True
    )
    submit = SubmitField('Se connecter')


class RegistrationForm(FlaskForm):
    # firstname = StringField('Prénom', validators=[DataRequired(), Length(1, 64)])
    # lastname = StringField('Nom', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[
        DataRequired(message='L\'email est requis'),
        Regexp(r'^[^@]+@[^@]+\.[^@]+$', message='Adresse email invalide')
    ])
    password = PasswordField('Mot de passe', validators=[DataRequired(message='Le mot de passe est requis.'), Length(min=8)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(message='La confirmation du mot de passe est requise.'), EqualTo('password', message='Les mots de passe ne correspondent pas.')
    ])
    submit = SubmitField('S\'inscrire')

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Cet email est déjà utilisé.')