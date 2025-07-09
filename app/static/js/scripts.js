window.funcionarioSeleccionado = null;
window.contextoModal = null;

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
        // 🔍 Búsqueda y selección de funcionario en modal "Buscar Funcionario"
    // let funcionarioSeleccionado = null;

    // Abrir modal al hacer clic en el botón principal
    //let contextoModal = null; // Global

    $('[data-target-context]').on('click', function () {
        contextoModal = $(this).data('target-context'); // ← Guarda el contexto
        $('#buscar-funcionario-input').val('');
        $('#resultado-busqueda').empty();
        $('#mensaje-no-encontrado').hide();
        $('#usar-funcionario-btn').prop('disabled', true);
        $('#modalBuscarFuncionario').modal('show');
    });


    // Buscar mientras se escribe
    $('#buscar-funcionario-input').on('input', function () {
        const query = $(this).val().trim();

        if (query.length < 3) {
            $('#resultado-busqueda').empty();
            $('#mensaje-no-encontrado').hide();
            $('#usar-funcionario-btn').prop('disabled', true);
            return;
        }

        $.get('/funcionarios/buscar', { query: query }, function (data) {
            const $tbody = $('#resultado-busqueda');
            $tbody.empty();
            funcionarioSeleccionado = null;
            $('#usar-funcionario-btn').prop('disabled', true);

            if (data.length === 0) {
                $('#mensaje-no-encontrado').show();
                return;
            }

            $('#mensaje-no-encontrado').hide();

            data.forEach(funcionario => {
                const row = `
                    <tr class="fila-funcionario" data-rut="${funcionario.rut}" data-nombre="${funcionario.nombre}" data-apellido="${funcionario.apellido}">
                        <td>${funcionario.rut}</td>
                        <td>${funcionario.nombre}</td>
                        <td>${funcionario.apellido}</td>
                    </tr>
                `;
                $tbody.append(row);
            });
        });
    });

    // Selección con clic
    $('#resultado-busqueda').on('click', '.fila-funcionario', function () {
        $('#resultado-busqueda tr').removeClass('table-primary');
        $(this).addClass('table-primary');

        funcionarioSeleccionado = {
            rut: $(this).data('rut'),
            nombre: $(this).data('nombre'),
            apellido: $(this).data('apellido')
        };

        $('#usar-funcionario-btn').prop('disabled', false);
    });

    // Doble clic = seleccionar directamente
    $('#resultado-busqueda').on('dblclick', '.fila-funcionario', function () {
        $(this).trigger('click');
        $('#usar-funcionario-btn').trigger('click');
    });

    // Usar funcionario seleccionado
    $('#usar-funcionario-btn').on('click', function () {
    console.log("🌐 Contexto activo al usar:", contextoModal);
    console.log("👤 Funcionario seleccionado al usar:", funcionarioSeleccionado);

    if (!funcionarioSeleccionado || !contextoModal) {
        console.warn("⚠️ No hay funcionario seleccionado o no hay contexto.");
        return;
    }

    if (contextoModal === 'alcaldia' && typeof window.seleccionarFuncionarioParaAlcaldia === 'function') {
        window.seleccionarFuncionarioParaAlcaldia(funcionarioSeleccionado);
    } else if (contextoModal === 'jefatura_daem' && typeof window.seleccionarFuncionarioParaJefaturaDaem === 'function') {
        window.seleccionarFuncionarioParaJefaturaDaem(funcionarioSeleccionado);
    } else if (contextoModal === 'orden_trabajo' && typeof window.seleccionarFuncionarioParaOrdenTrabajo === 'function') {
        window.seleccionarFuncionarioParaOrdenTrabajo(funcionarioSeleccionado);
    }


    const modal = bootstrap.Modal.getInstance(document.getElementById('modalBuscarFuncionario'));
    if (modal) modal.hide();
});


    
    // Inicializar tooltips de Bootstrap (poner al final del $(document).ready())
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    // 🌟 Función reutilizable para Alcaldía
    window.seleccionarFuncionarioParaAlcaldia = function (funcionario) {
        console.log("➡️ Funcionario seleccionado para Alcaldía:", funcionario);

        // Insertar datos en campos específicos del formulario de alcaldía
        const campoNombre = document.getElementById('nombre_alcalde');
        const campoRut = document.getElementById('rut_alcalde');

        if (campoNombre) campoNombre.value = `${funcionario.nombre} ${funcionario.apellido}`;
        if (campoRut) campoRut.value = funcionario.rut;

    };
    // 🌟 Función reutilizable para Jefatura DAEM
    window.seleccionarFuncionarioParaJefaturaDaem = function (funcionario) {
        console.log("➡️ Funcionario seleccionado para Jefatura DAEM:", funcionario);

        const campoNombre = document.getElementById('nombre_funcionario');
        const campoRut = document.getElementById('rut_funcionario');

        if (campoNombre) campoNombre.value = `${funcionario.nombre} ${funcionario.apellido}`;
        if (campoRut) campoRut.value = funcionario.rut;
    };
    window.seleccionarFuncionarioParaOrdenTrabajo = function (funcionario) {
        console.log("➡️ Funcionario seleccionado para Orden de Trabajo:", funcionario);

        if (funcionario.rut && funcionario.rut.includes('-')) {
            const partes = funcionario.rut.split('-');
            $('#rut_cuerpo').val(partes[0]);
            $('#rut_dv').val(partes[1]);
        }

        $('#nombre_funcionario').val(funcionario.nombre);
        $('#apellido_funcionario').val(funcionario.apellido);

        obtenerHorasYDetalle(); // ✅ Asegura que se carguen las horas al insertar
    };

    // ✅ Cargar horas disponibles automáticamente y mostrar detalle
function obtenerHorasYDetalle() {
    const rutCuerpo = $('#rut_cuerpo').val().trim();
    const rutDv = $('#rut_dv').val().trim().toUpperCase();

    if (rutCuerpo && rutDv) {
        const url = `/ordenes_trabajo/horas_disponibles/${rutCuerpo}-${rutDv}`;

        $.getJSON(url, function (data) {
            if (data.horas_disponibles !== undefined) {
                $('#horas_disponibles').val(data.horas_disponibles);
                window.detalleOrdenesActivas = data.detalle_ordenes || [];

                // Mostrar mensaje si no hay horas
                if (data.horas_disponibles === 0) {
                    $('#mensaje-horas').html(`
                        <div class="text-danger small fw-bold mt-1">
                            ❌ Sin horas disponibles. Revisa el <a href="#" id="link-ver-detalle">detalle de órdenes activas</a>.
                        </div>
                    `);
                } else {
                    $('#mensaje-horas').empty();
                }

                // Advertencia por tercera orden
                if (window.detalleOrdenesActivas.length > 2) {
                    $('#advertencia-tercera-orden').show();
                } else {
                    $('#advertencia-tercera-orden').hide();
                    $('#aceptar-implicaciones').prop('checked', false);
                }
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            console.error("❌ Error al obtener horas disponibles:", errorThrown);
        });
    }
}


    // Llamar función al perder foco en RUT o al completar desde modal
    $('#rut_cuerpo, #rut_dv').on('blur', obtenerHorasYDetalle);

    // Mostrar detalle de órdenes activas
    $('#ver-ordenes-activas-btn').on('click', function () {
        const rut = $('#rut_cuerpo').val() + '-' + $('#rut_dv').val();
        $('#modal-rut').text(rut);
        $('#modal-nombre').text($('#nombre_funcionario').val());
        $('#modal-apellido').text($('#apellido_funcionario').val());
        $('#modal-horas-disponibles').text($('#horas_disponibles').val());

        const tbody = $('#detalle-ordenes');
        tbody.empty();

        window.detalleOrdenesActivas.forEach(o => {
            const fila = `
                <tr>
                    <td>${o.numero_orden}</td>
                    <td>${o.colegio}</td>
                    <td>${o.horas}</td>
                    <td>${o.financiamiento}</td>
                    <td>${o.fecha_inicio}</td>
                    <td>${o.fecha_termino}</td>
                </tr>
            `;
            tbody.append(fila);
        });

        $('#modalOrdenesActivas').modal('show');
    });
    // Habilita click en el mensaje "Revisa el detalle..."
    $('#mensaje-horas').on('click', '#link-ver-detalle', function (e) {
        e.preventDefault();
        $('#ver-ordenes-activas-btn').trigger('click');
    });

});
