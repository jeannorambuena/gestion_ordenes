from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.auth.forms import LoginForm, RegisterForm
# from app.models import Usuario, db
from app.models import Usuario
from app.extensions.extensions import db


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Puedes ajustar esto según tu home
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(
            nombre_usuario=form.nombre_usuario.data).first()
        if usuario and usuario.check_password(form.contrasena.data):
            login_user(usuario)
            flash('Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(
            nombre_usuario=form.nombre_usuario.data).first()
        if usuario_existente:
            flash('El nombre de usuario ya existe.', 'warning')
            return redirect(url_for('auth.register'))
        nuevo_usuario = Usuario(nombre_usuario=form.nombre_usuario.data)
        nuevo_usuario.set_password(form.contrasena.data)
        nuevo_usuario.rol = 'cliente'  # Por defecto
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('auth.login'))
