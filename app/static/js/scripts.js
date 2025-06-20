// ✅ scripts.js con validación, redirección y control único de modal "Funcionario No Encontrado"

$(document).ready(function () {
    console.log("✅ scripts.js cargado correctamente");

    window.datosFuncionario = {};
    window.horasDisponiblesBackend = 0;
    window.detalleOrdenesActivas = [];

    function validarRutModulo11(rutCuerpo, rutDv) {
        if (!/^[0-9]{7,8}$/.test(rutCuerpo)) return false;
        if (!/^[0-9Kk]$/.test(rutDv)) return false;

        let suma = 0;
        let factor = 2;

        for (let i = rutCuerpo.length - 1; i >= 0; i--) {
            suma += parseInt(rutCuerpo[i]) * factor;
            factor = factor === 7 ? 2 : factor + 1;
        }

        const dvEsperado = 11 - (suma % 11);
        const dvCalculado = dvEsperado === 11 ? '0' : dvEsperado === 10 ? 'K' : dvEsperado.toString();

        return dvCalculado === rutDv.toUpperCase();
    }

    function limpiarRutYFoco(borrarTodo = true) {
        if (borrarTodo) $('#rut_cuerpo').val('');
        $('#rut_dv').val('');
        $('#rut_cuerpo').trigger('focus');
    }

    function limpiarFormularioYFoco() {
        $('#rut_cuerpo, #rut_dv, #nombre_funcionario, #apellido_funcionario, #telefono, #email, #direccion, #titulo').val('');
        $('#id_cargo').val('');
        $('#rut_cuerpo').prop('readonly', false);
        $('#rut_dv').prop('readonly', false);
        $('#rut_cuerpo').trigger('focus');
    }

    function cerrarModalCompleto(modal) {
        modal.hide();
        setTimeout(() => {
            document.body.classList.remove('modal-open');
            document.documentElement.style.overflow = '';
            document.body.style.overflow = '';
            $('.modal-backdrop').remove();
        }, 300);
    }

    function mostrarModalConFoco(modalId, focusId, borrarTodo = true) {
        const modalElement = document.getElementById(modalId);
        const modal = new bootstrap.Modal(modalElement);
        modal.show();

        $(`#${modalId} .btn-close, #${modalId} .btn-secondary`).off('click').on('click', function () {
            cerrarModalCompleto(modal);
            setTimeout(() => {
                limpiarRutYFoco(borrarTodo);
            }, 200);
        });
    }

    function mostrarModalEdicion(modalId) {
        const modalElement = document.getElementById(modalId);
        const modal = new bootstrap.Modal(modalElement);
        modal.show();

        $(`#${modalId} .btn-close, #${modalId} .btn-secondary`).off('click').on('click', function () {
            cerrarModalCompleto(modal);
            setTimeout(() => {
                limpiarFormularioYFoco();
            }, 200);
        });

        $(`#${modalId} #continuar-funcionario`).off('click').on('click', function () {
            $('#rut_cuerpo').prop('readonly', true);
            $('#rut_dv').prop('readonly', true);
            $('#nombre_funcionario').trigger('focus');
            cerrarModalCompleto(modal);
        });
    }

    function mostrarModalCrear(modalId) {
        const modalElement = document.getElementById(modalId);
        const modal = new bootstrap.Modal(modalElement);
        modal.show();

        $(`#${modalId} .btn-close, #${modalId} .btn-secondary`).off('click').on('click', function () {
            cerrarModalCompleto(modal);
            setTimeout(() => {
                limpiarFormularioYFoco();
            }, 200);
        });

        $(`#${modalId} #redirigir-nuevo`).off('click').on('click', function () {
            cerrarModalCompleto(modal);
            setTimeout(() => {
                const rutCuerpo = $('#rut_cuerpo').val().trim();
                const rutDv = $('#rut_dv').val().trim();
                const rutCompleto = `${rutCuerpo}-${rutDv}`;
                window.location.href = `/funcionarios/nuevo?rut=${encodeURIComponent(rutCompleto)}`;
            }, 300);
        });
    }

    function cargarDatosFuncionario(data) {
        window.datosFuncionario = data;
        $('#nombre_funcionario').val(data.nombre);
        $('#apellido_funcionario').val(data.apellido);
        $('#telefono').val(data.telefono);
        $('#email').val(data.email);
        $('#direccion').val(data.direccion);
        $('#titulo').val(data.titulo);
        $('#id_cargo').val(data.id_cargo);
        if ($('#nombre_alcalde').length) {
            $('#nombre_alcalde').val(`${data.nombre} ${data.apellido}`);
        }
    }

    $('#rut_dv').on('input', function () {
        const rutCuerpo = $('#rut_cuerpo').val().trim();
        const rutDv = $('#rut_dv').val().trim().toUpperCase();

        if (rutDv.length !== 1) return;

        if (!validarRutModulo11(rutCuerpo, rutDv)) {
            mostrarModalConFoco('modalRutInvalido', 'rut_cuerpo', true);
            return;
        }

        fetch('/validar_rut', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rut_cuerpo: rutCuerpo, rut_dv: rutDv })
        })
        .then(res => res.json())
        .then(data => {
            if (!data.valid) {
                mostrarModalConFoco('modalRutInvalido', 'rut_cuerpo', true);
                return;
            }

            if (data.existe) {
                cargarDatosFuncionario(data);
                mostrarModalEdicion('modalFuncionarioEncontrado');
            } else {
                mostrarModalCrear('modalFuncionarioNoEncontrado');
            }
        })
        .catch(err => {
            console.error("❌ Error en validación automática de RUT:", err);
        });
    });

    $('#continuar-funcionario').on('click', function () {
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalFuncionarioEncontrado'));
        if (modal) cerrarModalCompleto(modal);
    });
});
