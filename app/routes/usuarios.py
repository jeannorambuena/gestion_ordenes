from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.forms import UsuarioForm
from app.models import Usuario, Permiso
from app.extensions.extensions import db
from app.utils.roles_required import roles_required

usuarios_bp = Blueprint('usuarios', __name__)


# ===================== RUTAS PARA USUARIOS =====================


@usuarios_bp.route('/')
@login_required
@roles_required('administrador')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/list.html', usuarios=usuarios)


@usuarios_bp.route('/usuarios/permisos/<int:id>', methods=['GET', 'POST'])
def asignar_permisos(id):
    usuario = Usuario.query.get_or_404(id)
    todos_permisos = Permiso.query.all()

    if request.method == 'POST':
        # Recibir permisos seleccionados desde el formulario
        seleccionados = request.form.getlist('permisos')

        # Limpiar los permisos actuales
        usuario.permisos.clear()

        # Asignar los nuevos
        for permiso_id in seleccionados:
            permiso = Permiso.query.get(int(permiso_id))
            if permiso:
                usuario.permisos.append(permiso)

        db.session.commit()
        flash('Permisos actualizados correctamente.', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))

    return render_template('usuarios/permisos.html', usuario=usuario, todos_permisos=todos_permisos)


@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(
            nombre_usuario=form.nombre_usuario.data).first()
        if usuario_existente:
            flash('El nombre de usuario ya existe.', 'warning')
            return redirect(url_for('usuarios.nuevo_usuario'))
        nuevo_usuario = Usuario(nombre_usuario=form.nombre_usuario.data)
        nuevo_usuario.set_password(form.contraseña.data)
        # Asignación de rol directamente desde el formulario
        nuevo_usuario.rol = form.rol.data
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))
    return render_template('usuarios/nuevo.html', form=form)


@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nombre_usuario = form.nombre_usuario.data
        usuario.rol = form.rol.data
        if form.contrasena.data:
            usuario.set_password(form.contrasena.data)
        db.session.commit()
        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))
    return render_template('usuarios/editar.html', form=form, usuario=usuario)


@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))
