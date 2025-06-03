from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    nombre_usuario = StringField('Usuario', validators=[DataRequired()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


class RegisterForm(FlaskForm):
    nombre_usuario = StringField('Usuario', validators=[
                                 DataRequired(), Length(min=3, max=50)])
    contrasena = PasswordField('Contraseña', validators=[
                               DataRequired(), Length(min=6)])
    confirmar = PasswordField('Confirmar Contraseña', validators=[
                              DataRequired(), EqualTo('contrasena')])
    submit = SubmitField('Registrar')
