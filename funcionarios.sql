-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 01-07-2025 a las 00:14:56
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
-- Estructura de tabla para la tabla `funcionarios`
--

DROP TABLE IF EXISTS `funcionarios`;
CREATE TABLE IF NOT EXISTS `funcionarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellido` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `titulo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_cargo` int DEFAULT NULL,
  `rut_cuerpo` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rut_dv` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_rut_unico` (`rut_cuerpo`,`rut_dv`),
  KEY `id_cargo` (`id_cargo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `funcionarios`
--

INSERT INTO `funcionarios` (`id`, `nombre`, `apellido`, `direccion`, `telefono`, `titulo`, `id_cargo`, `rut_cuerpo`, `rut_dv`, `email`) VALUES
(1, 'Jean Paul', 'Norambuena Chávez', 'Ruta j55', '997718963', 'Ingeniero', 1, '14326078', 'k', NULL),
(2, 'Mariela Isabel', 'Farias Leyton', 'msaldfkslk', '997744887', 'educadora', 1, '15130287', '4', NULL),
(3, 'Luis Alfredo', 'Norambuena Cerda', 'Liquidambar 2045', '993241494', 'Profesor de Enseñanza Básica', 1, '6906337', '3', NULL),
(4, 'Maria Elena', 'Leyton Diaz', 'Isla Victoria 1914', '999999999', 'Profesora de Educacion Básica', 1, '7309224', '8', NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
