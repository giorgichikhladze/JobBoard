from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_wtf.file import FileAllowed
from models import User


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    remember = BooleanField('დამახსოვრება')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, max=20),
        Regexp(r'^\w+$', message="Username არ უნდა შეიცავდეს სფეისებს (მხოლოდ ასოები, ციფრები და _ )")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="გთხოვთ შეიყვანოთ სწორი ელ-ფოსტის მისამართი")
    ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=8, message="პაროლი უნდა იყოს მინიმუმ 8 სიმბოლო"),
                                 Regexp(r'^(?=.*[A-Z]).*$', message="პაროლი უნდა შეიცავდეს მინიმუმ ერთ დიდ ასოს")
                             ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('რეგისტრაცია')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ეს სახელი უკვე დაკავებულია.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('ეს მეილი უკვე გამოყენებულია.')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_file = FileField('პროფილის სურათი', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('განახლება')


class PostForm(FlaskForm):
    title = StringField('სათაური', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('აღწერა', validators=[DataRequired()])
    company = StringField('კომპანია', validators=[DataRequired()])
    location = StringField('მდებარეობა', validators=[DataRequired()])
    category = SelectField('კატეგორია', choices=[
        ('IT', 'IT & პროგრამირება'),
        ('Design', 'დიზაინი'),
        ('Marketing', 'მარკეტინგი'),
        ('Finance', 'ფინანსები'),
        ('Management', 'ადმინისტრაცია, მენეჯმენტი'),
        ('Sales', 'გაყიდვები'),
        ('Technical', 'ზოგადი ტექნიკური პერსონალი'),
        ('Construction', 'მშენებლობა, რემონტი'),
        ('Distribution', 'დისტრიბუცია'),
        ('Medicine', 'მედიცინა'),
        ('Other', 'სხვა')
    ], validators=[DataRequired()])
    salary = StringField('ხელფასი', validators=[DataRequired()])
    submit = SubmitField('გამოქვეყნება')
