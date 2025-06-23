-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 23-06-2025 a las 07:41:35
-- Versión del servidor: 8.3.0
-- Versión de PHP: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestion_ordenes`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alcaldia`
--

DROP TABLE IF EXISTS `alcaldia`;
CREATE TABLE IF NOT EXISTS `alcaldia` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rut_cuerpo` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rut_dv` char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_termino` date DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_cargo` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_rut_alcaldia` (`rut_cuerpo`,`rut_dv`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `alcaldia`
--

INSERT INTO `alcaldia` (`id`, `rut_cuerpo`, `rut_dv`, `fecha_inicio`, `fecha_termino`, `email`, `telefono`, `id_cargo`) VALUES
(5, '7309224', '8', '2025-06-02', '2025-06-30', NULL, '999999999', 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargos`
--

DROP TABLE IF EXISTS `cargos`;
CREATE TABLE IF NOT EXISTS `cargos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_cargo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `cargos`
--

INSERT INTO `cargos` (`id`, `nombre_cargo`, `descripcion`) VALUES
(1, 'Profesor', 'Encargado de impartir clases a los estudiante'),
(5, 'Asistente de Aula', 'Asistente de Aula '),
(6, 'Director', 'Director de Comalle'),
(7, 'Fonoaudiólogo', 'Profesional de la Salud'),
(8, 'Alcalde', 'Máxima autoridad comunal'),
(9, 'Alcaldesa', 'Máxima autoridad comunal'),
(10, 'Alcalde(S)', 'Alcalde subrogante'),
(11, 'Alcaldesa(S)', 'Alcaldesa subrogante'),
(16, 'Jefe DAEM', 'Encargado principal del Departamento de Administración de Educación Municipal'),
(17, 'Jefe DAEM(S)', 'Jefe DAEM subrogante temporal'),
(18, 'Jefe DAEM(R)', 'Jefe DAEM reemplazante por periodo determinado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `colegios`
--

DROP TABLE IF EXISTS `colegios`;
CREATE TABLE IF NOT EXISTS `colegios` (
  `rbd` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_colegio` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `director` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tipo_ensenanza` enum('BASICA','MEDIA') COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitud` decimal(10,8) DEFAULT NULL,
  `longitud` decimal(11,8) DEFAULT NULL,
  PRIMARY KEY (`rbd`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `colegios`
--

INSERT INTO `colegios` (`rbd`, `nombre_colegio`, `direccion`, `telefono`, `director`, `email`, `tipo_ensenanza`, `latitud`, `longitud`) VALUES
('2795-2', 'Escuela D-56 Teno(PRIMER CICLO)', 'LAUTARO 390 TENO', '56956490435', 'Miguel Urbina', 'escuelateno@daemteno.cl', 'BASICA', -34.87187576, -71.16059875),
('2809-6', 'Escuela G-59 Las Liras', 'CAMINO A LAS LIRAS S/N', '56956490431', 'nn', 'lasliras@daemteno.cl', 'BASICA', -34.86644363, -71.02109528),
('2800-2', 'Escuela F-60 Morza', 'CAMINO PRINCIPAL MORZA S/N', '56956490432', 'nn', 'morza@daemteno.cl', 'BASICA', -34.82292938, -71.01967621),
('2796-0', 'Escuela E-61 Comalle', 'PUEBLO DE COMALLE', '56951886597', 'Francisco Zúñiga', 'comalle@daemteno.cl', 'BASICA', -34.84877396, -71.26980591),
('0504-4', 'Escuela E-63 Hda. Teno', 'SECTOR HACIENDA DE TENO', '56952095196', 'Luisa Silva', 'haciendadeteno@daemteno.cl', 'BASICA', -34.87365723, -71.22540283),
('2801-0', 'Escuela F-64 Monterilla', 'Long.sur Km.165 Monterilla', '56956386135', 'nn', 'monterilla@daemteno.cl', 'BASICA', -34.82242203, -71.06935120),
('2802-9', 'Escuela F-65 Santa Susana', 'Camino La Montana Km.11, Santa Susana', '56975281251', 'nn', 'susanamontes@daemteno.cl', 'BASICA', -34.92112350, -71.02867889),
('2803-7', 'Escuela F-68 Las Arboledas', 'Ruta J-40 Kilometro 5.5 Camino A Comalle', '56988195580', 'Jaime Herrera', 'lasarboledas@daemteno.cl', 'BASICA', -34.86196136, -71.19743347),
('2804-5', 'Escuela F-69 La Laguna', 'Camino La Montaña Sector La Laguna Km 17 393', '56965945701', 'nn', 'lalaguna@daemteno.cl', 'BASICA', -34.95909500, -70.97148895),
('2805-3', 'Escuela F-70 V. del Bajo', 'Ventana Del Bajo S/n Camino Los Lagartos Km 10', '56956490434', 'Marcelo Fierro', 'ventanadelbajo@daemteno.cl', 'BASICA', -34.91666031, -71.07469940),
('2806-1', 'Escuela F-72 Huemul', 'Viña Huemul A 08 Km. De Morza Hacia La Cordillera', '56966756889', 'nn', 'huemul@daemteno.cl', 'BASICA', -34.87733078, -70.95379639),
('2814-2', 'Escuela G-74 San Rafael', 'Long. Sur Km. 170', '56956395466', 'Pamela Peñaloza', 'sanrafael@daemteno.cl', 'BASICA', -34.83979034, -71.10267639),
('2816-9', 'Escuela G-76 Santa Rebeca', 'Santa Rebeca S/n Teno', '56975280591', 'Marisol Navarro', 'sanrarebeca@daemteno.cl', 'BASICA', -34.86664200, -71.06790924),
('2817-7', 'Escuela G-77 San Cristobal', 'Longitudinal Sur Km. 176', '56966760375', 'Claudio Vergara', 'sancristobal@daemteno.cl', 'BASICA', -34.88217545, -71.14791107),
('2819-3', 'Escuela G-79 Teniente Cruz', 'Camino Los Lagartos S/n,', '56962182562', 'Nilda Arias Navarro', 'tenientecruz@daemteno.cl', 'BASICA', -34.89501190, -71.11250305),
('2820-7', 'Escuela G-85 Los Alisos', 'Camino Publico S/n Los Alisos - Teno', '56956490433', 'Claudia Gallegos', 'losalisos@daemteno.cl', 'BASICA', -34.90025330, -71.25875854),
('11352-2', 'Escuela G-755 El Guindo', 'Camino Publico S/n El Guindo', '56956391601', 'Alvaro Cotapo Gomez', 'elguindo@daemteno.cl', 'BASICA', -34.85538483, -71.33351135),
('2794-4', 'Liceo C-4 de Teno', 'Dr. Faundez 380', '56951885210', 'nn', 'liceo@liceoteno.cl', 'MEDIA', -34.86979675, -71.16536713);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `financiamiento`
--

DROP TABLE IF EXISTS `financiamiento`;
CREATE TABLE IF NOT EXISTS `financiamiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_financiamiento` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `financiamiento`
--

INSERT INTO `financiamiento` (`id`, `nombre_financiamiento`) VALUES
(6, 'SEP'),
(2, 'PIE'),
(3, 'REGULAR'),
(4, 'FAEP');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `funcionarios`
--

DROP TABLE IF EXISTS `funcionarios`;
CREATE TABLE IF NOT EXISTS `funcionarios` (
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellido` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `titulo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_cargo` int DEFAULT NULL,
  `rut_cuerpo` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rut_dv` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`rut_cuerpo`,`rut_dv`),
  KEY `id_cargo` (`id_cargo`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `funcionarios`
--

INSERT INTO `funcionarios` (`nombre`, `apellido`, `direccion`, `telefono`, `titulo`, `id_cargo`, `rut_cuerpo`, `rut_dv`, `email`) VALUES
('Maria Elena', 'Leyton Diaz', 'Isla Victoria 1914', '999999999', 'Profesora de Educacion Básica', 1, '7309224', '8', NULL),
('Mariela Isabel', 'Farias Leyton', 'msaldfkslk', '997744887', 'educadora', 1, '15130287', '4', NULL),
('Jean Paul', 'Norambuena Chávez', 'Ruta j55', '997718963', 'Ingeniero', 1, '14326078', 'k', NULL),
('Luis Alfredo', 'Norambuena Cerda', 'Liquidambar 2045', '993241494', 'Profesor de Enseñanza Básica', 1, '6906337', '3', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `funcionarios_backup`
--

DROP TABLE IF EXISTS `funcionarios_backup`;
CREATE TABLE IF NOT EXISTS `funcionarios_backup` (
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellido` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `titulo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_cargo` int DEFAULT NULL,
  `rut_cuerpo` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rut_dv` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `funcionarios_backup`
--

INSERT INTO `funcionarios_backup` (`nombre`, `apellido`, `direccion`, `telefono`, `titulo`, `id_cargo`, `rut_cuerpo`, `rut_dv`, `email`) VALUES
('Maria Elena', 'Leyton Diaz', 'Isla Victoria 1914', '999999999', 'Profesora de Educacion Básica', 1, '7309224', '8', NULL),
('Mariela Isabel', 'Farias Leyton', 'msaldfkslk', '997744887', 'educadora', 1, '15130287', '4', NULL),
('Jean Paul', 'Norambuena Chávez', 'Ruta j55', '997718963', 'Ingeniero', 1, '14326078', 'k', NULL),
('Luis Alfredo', 'Norambuena Cerda', 'Liquidambar 2045', '993241494', 'Profesor de Enseñanza Básica', 1, '6906337', '3', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `funcionarios_colegios`
--

DROP TABLE IF EXISTS `funcionarios_colegios`;
CREATE TABLE IF NOT EXISTS `funcionarios_colegios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `funcionario_id` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `colegio_rbd` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `horas_disponibles` int NOT NULL,
  `orden_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `funcionario_id` (`funcionario_id`),
  KEY `colegio_id` (`colegio_rbd`),
  KEY `orden_id` (`orden_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `funcionarios_colegios`
--

INSERT INTO `funcionarios_colegios` (`id`, `funcionario_id`, `colegio_rbd`, `horas_disponibles`, `orden_id`) VALUES
(7, '15130287', '2816-9', 15, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `funcionario_financiamiento`
--

DROP TABLE IF EXISTS `funcionario_financiamiento`;
CREATE TABLE IF NOT EXISTS `funcionario_financiamiento` (
  `funcionario_id` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `financiamiento_id` int NOT NULL,
  PRIMARY KEY (`funcionario_id`,`financiamiento_id`),
  KEY `financiamiento_id` (`financiamiento_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_cambios`
--

DROP TABLE IF EXISTS `historial_cambios`;
CREATE TABLE IF NOT EXISTS `historial_cambios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tabla_afectada` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `registro_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `tipo_cambio` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `detalle_cambio` text COLLATE utf8mb4_unicode_ci,
  `fecha_cambio` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_contratos`
--

DROP TABLE IF EXISTS `historial_contratos`;
CREATE TABLE IF NOT EXISTS `historial_contratos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cedula_identidad` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero_orden` int NOT NULL,
  `colegio_rbd` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_termino` date DEFAULT NULL,
  `es_indefinido` tinyint(1) DEFAULT '0',
  `tipo_contrato` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `horas_disponibles` int NOT NULL,
  `remuneracion` decimal(10,2) DEFAULT NULL,
  `motivo_termino` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion_puesto` text COLLATE utf8mb4_unicode_ci,
  `beneficios` text COLLATE utf8mb4_unicode_ci,
  `estado` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Activo',
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_modificacion` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `cedula_identidad` (`cedula_identidad`),
  KEY `numero_orden` (`numero_orden`),
  KEY `colegio_rbd` (`colegio_rbd`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horas_disponibles`
--

DROP TABLE IF EXISTS `horas_disponibles`;
CREATE TABLE IF NOT EXISTS `horas_disponibles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `horas_disponibles` int NOT NULL,
  `fecha_asignacion` date NOT NULL,
  `funcionario_id` varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `funcionario_dv` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `colegio_rbd` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `funcionario_id` (`funcionario_id`,`funcionario_dv`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jefatura_daem`
--

DROP TABLE IF EXISTS `jefatura_daem`;
CREATE TABLE IF NOT EXISTS `jefatura_daem` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rut_cuerpo` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rut_dv` char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_cargo` int NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_termino` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_rut_daem` (`rut_cuerpo`,`rut_dv`),
  KEY `fk_jefatura_cargo` (`id_cargo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `jefatura_daem`
--

INSERT INTO `jefatura_daem` (`id`, `rut_cuerpo`, `rut_dv`, `id_cargo`, `fecha_inicio`, `fecha_termino`) VALUES
(2, '14326078', 'k', 16, '2025-06-01', '2025-06-30');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenes_trabajo`
--

DROP TABLE IF EXISTS `ordenes_trabajo`;
CREATE TABLE IF NOT EXISTS `ordenes_trabajo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_inicio` date NOT NULL,
  `fecha_termino` date DEFAULT NULL,
  `es_indefinido` tinyint(1) DEFAULT '0',
  `colegio_rbd` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `reemplazo_a` varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `motivo_reemplazo` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rut_cuerpo` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rut_dv` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `financiamiento_id` int DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_modificacion` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `numero_orden` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo_contrato_id` int DEFAULT NULL,
  `horas_disponibles` int DEFAULT '0',
  `anio` int NOT NULL,
  `alcalde_id` int NOT NULL,
  `jefatura_daem_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_orden` (`numero_orden`),
  KEY `colegio_rbd` (`colegio_rbd`),
  KEY `fk_financiamiento` (`financiamiento_id`),
  KEY `fk_tipo_contrato` (`tipo_contrato_id`),
  KEY `fk_orden_alcalde` (`alcalde_id`),
  KEY `fk_orden_jefatura` (`jefatura_daem_id`)
) ENGINE=MyISAM AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `ordenes_trabajo`
--

INSERT INTO `ordenes_trabajo` (`id`, `fecha_inicio`, `fecha_termino`, `es_indefinido`, `colegio_rbd`, `observaciones`, `reemplazo_a`, `motivo_reemplazo`, `rut_cuerpo`, `rut_dv`, `financiamiento_id`, `fecha_creacion`, `fecha_modificacion`, `numero_orden`, `tipo_contrato_id`, `horas_disponibles`, `anio`, `alcalde_id`, `jefatura_daem_id`) VALUES
(68, '2025-06-02', '2025-06-27', 0, '2795-2', 'No existen observaciones', NULL, NULL, '7309224', '8', 3, '2025-05-25 15:56:27', '2025-06-21 15:04:22', '1', 4, 10, 2025, 0, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

DROP TABLE IF EXISTS `permisos`;
CREATE TABLE IF NOT EXISTS `permisos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id`, `nombre`, `descripcion`) VALUES
(1, 'ver_ordenes', 'Puede ver las órdenes de trabajo'),
(2, 'crear_orden', 'Puede crear nuevas órdenes'),
(3, 'editar_orden', 'Puede editar órdenes existentes'),
(4, 'ver_jefatura', 'Puede acceder a datos de jefatura DAEM'),
(5, 'ver_alcaldia', 'Puede acceder a datos de alcaldía'),
(6, 'ver_usuarios', 'Puede ver y editar usuarios'),
(7, 'administrar_permisos', 'Puede asignar roles y permisos'),
(8, 'editar_usuarios', 'Puede editar datos de usuarios');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_rol` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_rol` (`nombre_rol`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `nombre_rol`, `descripcion`) VALUES
(3, 'Administrador', 'Control total sistema'),
(4, 'usuario', 'control limitado del sistema');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles_permisos`
--

DROP TABLE IF EXISTS `roles_permisos`;
CREATE TABLE IF NOT EXISTS `roles_permisos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rol` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `permiso_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `permiso_id` (`permiso_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_contrato`
--

DROP TABLE IF EXISTS `tipo_contrato`;
CREATE TABLE IF NOT EXISTS `tipo_contrato` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `observacion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `tipo_contrato`
--

INSERT INTO `tipo_contrato` (`id`, `nombre`, `observacion`) VALUES
(4, 'Código del Trabajo', 'Ley Nro XXXXXXX'),
(5, 'Estatuto Docente', 'XX'),
(6, 'Honorarios', ''),
(7, 'Planta', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contrasena_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rol_id` int DEFAULT NULL,
  `rol` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Usuario',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre_usuario`, `contrasena_hash`, `rol_id`, `rol`) VALUES
(2, 'jeannorambuena', 'pbkdf2:sha256:600000$82paJv3QIe7S8dOq$d212fa99dd9d8a949fd54271e23ab78ff6dd7d460404346e5c1147a0b3875235', 3, 'Administrador'),
(4, 'cliente', 'scrypt:32768:8:1$UqiBiioacTBzphrS$d4f344133a0432385ce5298908b551a790bc7a8919eaf964f6564d2b6eb7050be3f7af655f9f5b571a5226bad3880f10a223676f2a3767945ccab469b2fac533', 4, 'Usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_permisos`
--

DROP TABLE IF EXISTS `usuario_permisos`;
CREATE TABLE IF NOT EXISTS `usuario_permisos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `permiso_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`,`permiso_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `jefatura_daem`
--
ALTER TABLE `jefatura_daem`
  ADD CONSTRAINT `fk_jefatura_cargo` FOREIGN KEY (`id_cargo`) REFERENCES `cargos` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
