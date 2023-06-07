from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from twizzle.queries import get_user_by_name, get_user_by_email
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                    validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = get_user_by_name(username.data)
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
        
    def validate_email(self, email):
        user = get_user_by_email(email.data)
        if user:
            raise ValidationError('That email is already in use. Please use a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                    validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.user_name:
            user = get_user_by_name(username.data)
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')
        
    def validate_email(self, email):
        if email.data != current_user.email_address:
            user = get_user_by_email(email.data)
            if user:
                raise ValidationError('That email is already in use. Please use a different one')



class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = get_user_by_email(email.data)
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')