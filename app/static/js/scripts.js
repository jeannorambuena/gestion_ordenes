$(document).ready(function () {
    console.log("✅ jQuery está listo, ejecutando scripts.js");

    window.datosFuncionario = {};
    window.horasDisponiblesBackend = 0;
    window.detalleOrdenesActivas = [];

    $('#rut_dv').on('input', async function () {
        const rutCuerpo = $('#rut_cuerpo').val().trim();
        const rutDv = $('#rut_dv').val().trim().toUpperCase();

        if (!rutCuerpo || !rutDv) return;

        try {
            const response = await fetch('/ordenes_trabajo/validar_rut_endpoint', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ rut_cuerpo: rutCuerpo, rut_dv: rutDv }),
            });

            const data = await response.json();
            console.log("📥 Respuesta del backend:", data);

            if (!data.valid) {
                new bootstrap.Modal(document.getElementById("modalRutInvalido")).show();
                return;
            }

            if (data.existe) {
                window.datosFuncionario = { rut_cuerpo: rutCuerpo, rut_dv: rutDv, nombre: data.nombre, apellido: data.apellido };
                $('#nombre_funcionario').val(data.nombre);
                $('#apellido_funcionario').val(data.apellido);
            
                // Llamamos a la función de validación y dejamos que ella decida si mostrar el modal o no
                validarHorasFuncionario(rutCuerpo, rutDv);
            
                return; // ⛔ Importante: salimos aquí y no mostramos nada más
            }
            

        } catch (error) {
            console.error("❌ Error en la petición fetch:", error);
        }
    });

    function validarHorasFuncionario(rutCuerpo, rutDv) {
        $.ajax({
            url: '/ordenes_trabajo/validar_horas_funcionario',
            method: 'GET',
            data: { rut_cuerpo: rutCuerpo, rut_dv: rutDv },
            success: function (data) {
                console.log("🧮 Validación de horas:", data);
    
                $('#horas_disponibles').val(data.horas_disponibles);
                window.horasDisponiblesBackend = data.horas_disponibles;
                window.detalleOrdenesActivas = data.ordenes_activas || [];
    
                if (data.horas_disponibles <= 0) {
                    $('#horas_disponibles').val(0);  // Mostrar 0 en el campo
    
                    // Actualizar tabla con órdenes activas
                    const tbody = $('#detalle-horas-modal');
                    tbody.empty();
    
                    if (data.ordenes_activas.length === 0) {
                        tbody.append('<tr><td colspan="6">No hay órdenes activas.</td></tr>');
                    } else {
                        data.ordenes_activas.forEach(ord => {
                            tbody.append(`
                                <tr>
                                    <td>${ord.numero_orden}</td>
                                    <td>${ord.colegio}</td>
                                    <td>${ord.horas}</td>
                                    <td>${ord.financiamiento}</td>
                                    <td>${ord.fecha_inicio}</td>
                                    <td>${ord.fecha_termino}</td>
                                </tr>`);
                        });
                    }
    
                    $('#horas-asignadas-modal').text(data.horas_totales);
    
                    // Mostrar solo este modal
                    const modal = new bootstrap.Modal(document.getElementById("modalSinHoras"));
                    modal.show();
    
                    // 🚫 No continuar con más lógica
                    return;
                }
    
                // ✅ Si tiene horas disponibles, mostramos el modal de "Funcionario encontrado"
                new bootstrap.Modal(document.getElementById("modalFuncionarioEncontrado")).show();
            },
            error: function () {
                console.error("❌ Error al validar las horas del funcionario");
            }
        });
    }
    

    $('#ver-ordenes-activas-btn').on('click', function () {        const detalle = window.detalleOrdenesActivas;
        const rut = $('#rut_cuerpo').val() + '-' + $('#rut_dv').val();
        const nombre = $('#nombre_funcionario').val();
        const apellido = $('#apellido_funcionario').val();

        $('#modal-rut').text(rut);
        $('#modal-nombre').text(nombre);
        $('#modal-apellido').text(apellido);
        $('#modal-horas-disponibles').text(window.horasDisponiblesBackend);

        const tbody = $('#detalle-ordenes');
        tbody.empty();

        if (detalle.length === 0) {
            tbody.append('<tr><td colspan="6">No hay órdenes activas.</td></tr>');
        } else {
            detalle.forEach(ord => {
                tbody.append(`
                    <tr>
                        <td>${ord.numero_orden}</td>
                        <td>${ord.colegio}</td>
                        <td>${ord.horas}</td>
                        <td>${ord.financiamiento}</td>
                        <td>${ord.fecha_inicio}</td>
                        <td>${ord.fecha_termino}</td>
                    </tr>`);
            });
        }

        new bootstrap.Modal(document.getElementById("modalOrdenesActivas")).show();
    });

    $('#horas_disponibles').on('input', function () {
        const horasIngresadas = parseInt($(this).val());
        const mensajeDiv = $('#mensaje-horas');
        const botonGuardar = $('#guardar-btn');

        if (isNaN(horasIngresadas)) {
            mensajeDiv.html('<span class="text-danger">❌ Ingresa un número válido de horas.</span>');
            botonGuardar.prop('disabled', true);
            return;
        }

        if (horasIngresadas > window.horasDisponiblesBackend) {
            mensajeDiv.html(`<span class="text-danger">❌ No puedes asignar más de ${window.horasDisponiblesBackend} horas disponibles.</span>`);
            botonGuardar.prop('disabled', true);
        } else {
            mensajeDiv.html('');
            botonGuardar.prop('disabled', false);
        }
    });

    $('#modalRutInvalido').on('hidden.bs.modal', function () {
        $('#rut_cuerpo').val('').focus();
        $('#rut_dv').val('');
    });

    $('#cerrar-funcionario-no-encontrado, #cancelar-funcionario-no-encontrado').on('click', function () {
        $('#rut_cuerpo').val('').focus();
        $('#rut_dv').val('');
    });

    $('#redirigir-nuevo').on('click', function () {
        window.location.href = "/funcionarios/nuevo";
    });

    $('#cerrar-funcionario-encontrado').on('click', function () {
        limpiarCampos();
        cerrarModal('modalFuncionarioEncontrado');
        setTimeout(() => { $('#rut_cuerpo').focus(); }, 300);
    });

    $('#continuar-funcionario').on('click', function () {
        $('#rut_cuerpo').val(window.datosFuncionario.rut_cuerpo);
        $('#rut_dv').val(window.datosFuncionario.rut_dv);
        $('#nombre_funcionario').val(window.datosFuncionario.nombre);
        $('#apellido_funcionario').val(window.datosFuncionario.apellido);
        cerrarModal('modalFuncionarioEncontrado');
        setTimeout(() => { $('#colegio_rbd').focus(); }, 300);
    });

    function cerrarModal(modalId) {
        const modalElement = document.getElementById(modalId);
        if (!modalElement) return;

        let modalInstance = bootstrap.Modal.getInstance(modalElement);
        if (!modalInstance) modalInstance = new bootstrap.Modal(modalElement);
        modalInstance.hide();

        setTimeout(() => {
            $('.modal-backdrop').remove();
            $('body').removeClass('modal-open').css('overflow', 'auto');
            modalElement.classList.remove("show");
            modalElement.style.display = "none";
            modalElement.setAttribute("aria-hidden", "true");
        }, 500);
    }

    function limpiarCampos() {
        $('#rut_cuerpo, #rut_dv, #nombre_funcionario, #apellido_funcionario, #colegio_rbd, #tipo_contrato, #financiamiento_id, #fecha_inicio, #fecha_termino, #horas_disponibles, #observaciones').val('');
        $('#mensaje-horas').html('');
        $('#guardar-btn').prop('disabled', false);
    }

    $('#modalFuncionarioNoEncontrado').on('hidden.bs.modal', function () {
        limpiarCampos();
    });

    $('#buscar-funcionario-btn').on('click', function () {
        const modalElement = document.getElementById("modalBuscarFuncionario");
        if (!modalElement) return;
        let modalInstance = new bootstrap.Modal(modalElement);
        modalInstance.show();
    });

    $('#modalBuscarFuncionario').on('shown.bs.modal', function () {
        $('#buscar-funcionario-input').val('');
        $('#resultado-busqueda').empty();
        $('#mensaje-no-encontrado').hide();
        setTimeout(() => { $('#buscar-funcionario-input').focus(); }, 300);
    });

    $('#modalBuscarFuncionario').on('hidden.bs.modal', function () {
        $('#buscar-funcionario-input').val('');
        $('#resultado-busqueda').empty();
        $('#mensaje-no-encontrado').hide();
        setTimeout(() => { $('#rut_cuerpo').focus(); }, 300);
    });

    $('#buscar-funcionario-input').on('input', function () {
        let query = $(this).val().trim();
        if (query.length < 3) {
            $('#resultado-busqueda').empty();
            $('#mensaje-no-encontrado').hide();
            return;
        }

        $.ajax({
            url: '/ordenes_trabajo/buscar_funcionario',
            method: 'GET',
            data: { q: query },
            success: function (response) {
                $('#resultado-busqueda').empty();
                if (response.length === 0) {
                    $('#mensaje-no-encontrado').show();
                } else {
                    $('#mensaje-no-encontrado').hide();
                    response.forEach(funcionario => {
                        $('#resultado-busqueda').append(`
                            <tr class="seleccionar-funcionario" data-rut="${funcionario.rut}" data-nombre="${funcionario.nombre}" data-apellido="${funcionario.apellido}">
                                <td>${funcionario.rut}</td>
                                <td>${funcionario.nombre}</td>
                                <td>${funcionario.apellido}</td>
                            </tr>`);
                    });
                }
            },
            error: function () {
                console.error("❌ Error en la solicitud AJAX");
            }
        });
    });

    $(document).on('click', '.seleccionar-funcionario', function () {
        $('.seleccionar-funcionario').removeClass('table-primary');
        $(this).addClass('table-primary');

        $('#usar-funcionario-btn').data('rut', $(this).data('rut'));
        $('#usar-funcionario-btn').data('nombre', $(this).data('nombre'));
        $('#usar-funcionario-btn').data('apellido', $(this).data('apellido'));
        $('#usar-funcionario-btn').prop('disabled', false);
    });

    $('#usar-funcionario-btn').on('click', function () {
        const rut = $(this).data('rut');
        const nombre = $(this).data('nombre');
        const apellido = $(this).data('apellido');

        if (!rut || !nombre || !apellido) return;

        const [rutCuerpo, rutDv] = rut.split('-');
        $('#rut_cuerpo').val(rutCuerpo);
        $('#rut_dv').val(rutDv);
        $('#nombre_funcionario').val(nombre);
        $('#apellido_funcionario').val(apellido);

        validarHorasFuncionario(rutCuerpo, rutDv);

        cerrarModal('modalBuscarFuncionario');
        setTimeout(() => { $('#colegio_rbd').focus(); }, 300);
    });
    // Cuando se cierre el modal "Sin Horas", se limpian los campos y se devuelve el foco al RUT
$('#modalSinHoras').on('hidden.bs.modal', function () {
    limpiarCampos();
    setTimeout(() => { $('#rut_cuerpo').focus(); }, 300);
});

});
