from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class inscriptionForm(FlaskForm):
    """ form pour l'inscription """
    username = StringField('username_label', validators=[InputRequired(message="username requis"), Length(min=4, max=25, message="le message doit etre entre 4 et 25 char")])
    
    password = PasswordField('password_label', validators=[InputRequired(message="Password requis"), Length(min=4, max=25, message="le Password doit etre entre 4 et 25 char")])
    
    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password requis"), EqualTo('password', message="les mots de passe doivent être identiques")])
   
    bouton_submit = SubmitField('creation')
