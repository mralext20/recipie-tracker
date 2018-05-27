from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, equal_to, ValidationError
from app.models import Chef


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit_button = SubmitField('Login', validators=[DataRequired()])


class SignupForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    displayname = StringField('Display Name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('password, again', validators=[DataRequired(), equal_to('password')])
    remember_me = BooleanField('Remember Me')
    submit_button = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Chef.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class RecipeForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    ingredients = TextAreaField('ingredients', validators=[DataRequired()])
    instructions = TextAreaField('directions', validators=[DataRequired()])
    submit_button = SubmitField('Post')
