-- crear usuarios

CREATE USER 'Admin'@'localhost' IDENTIFIED BY '123';

GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES, CREATE, DROP, ALTER, INDEX, TRIGGER, REPLICATION CLIENT, REPLICATION SLAVE, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EXECUTE, RELOAD, SHUTDOWN, FILE, PROCESS, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, SHOW DATABASES, CREATE USER, GRANT OPTION, EVENT, CREATE TABLESPACE ON *.* TO 'Admin'@'localhost';

FLUSH PRIVILEGES;

CREATE USER 'Gerente'@'localhost' IDENTIFIED BY '123';

GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES, CREATE, DROP, ALTER, INDEX, TRIGGER, REPLICATION CLIENT, REPLICATION SLAVE, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EXECUTE, RELOAD, SHUTDOWN, FILE, PROCESS, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, SHOW DATABASES, CREATE USER, GRANT OPTION, EVENT, CREATE TABLESPACE ON *.* TO 'Admin'@'localhost';

FLUSH PRIVILEGES;


CREATE USER 'Cajero'@'localhost' IDENTIFIED BY '123';

GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES, CREATE, DROP, ALTER, INDEX, TRIGGER, REPLICATION CLIENT, REPLICATION SLAVE, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EXECUTE, RELOAD, SHUTDOWN, FILE, PROCESS, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, SHOW DATABASES, CREATE USER, GRANT OPTION, EVENT, CREATE TABLESPACE ON *.* TO 'Admin'@'localhost';

FLUSH PRIVILEGES;





-- CREAR INDICES UNICOS (VALIDAR EN BD)

-- para tel del intermediario
ALTER TABLE `proyecto`.`intermediario`
ADD UNIQUE INDEX `intermediario_TEL_idx` (`TEL`) USING BTREE;


-- para el correo de los usuarios
ALTER TABLE `proyecto`.`usuarios`
ADD UNIQUE INDEX `usuarios_CORREO_idx` (`CORREO`) USING BTREE;





-- llenar datos

-- FECHAS
INSERT INTO dia (ID_DIA, DIA) VALUES
(1, '1'),
(2, '2'),
(3, '3'),
(4, '4'),
(5, '5'),
(6, '6'),
(7, '7'),
(8, '8'),
(9, '9'),
(10, '10'),
(11, '11'),
(12, '12'),
(13, '13'),
(14, '14'),
(15, '15'),
(16, '16'),
(17, '17'),
(18, '18'),
(19, '19'),
(20, '20'),
(21, '21'),
(22, '22'),
(23, '23'),
(24, '24'),
(25, '25'),
(26, '26'),
(27, '27'),
(28, '28'),
(29, '29'),
(30, '30'),
(31, '31');

INSERT INTO mes (ID_MES, MES) VALUES
(1, 'Enero'),
(2, 'Febrero'),
(3, 'Marzo'),
(4, 'Abril'),
(5, 'Mayo'),
(6, 'Junio'),
(7, 'Julio'),
(8, 'Agosto'),
(9, 'Septiembre'),
(10, 'Octubre'),
(11, 'Noviembre'),
(12, 'Diciembre');


INSERT INTO anio (ID_ANIO, ANIO) VALUES
(1, '2020'),
(2, '2021'),
(3, '2022'),
(4, '2023'),
(5, '2024'),
(6, '2025'),
(7, '2026'),
(8, '2027'),
(9, '2028'),
(10, '2029'),
(11, '2030');

-- VENTAS

INSERT INTO ventas (ID_VENTA, CANTIDAD_VENTA, TOTAL, ESTATUS, ID_DIA, ID_MES, ID_ANIO) VALUES
(1, 5, 75.00, '1', 1, 1, 1),   -- 5 unidades vendidas el 1 de enero de 2024
(2, 10, 150.00, '1', 2, 1, 1),  -- 10 unidades vendidas el 2 de enero de 2024
(3, 3, 45.00, '1', 3, 1, 1),    -- 3 unidades vendidas el 3 de enero de 2024
(4, 7, 105.00, '1', 4, 1, 1),   -- 7 unidades vendidas el 4 de enero de 2024
(5, 1, 15.00, '1', 5, 1, 1),    -- 1 unidad vendida el 5 de enero de 2024
(6, 12, 180.00, '1', 6, 1, 1),   -- 12 unidades vendidas el 6 de enero de 2024
(7, 4, 60.00, '1', 7, 1, 1),     -- 4 unidades vendidas el 7 de enero de 2024
(8, 9, 135.00, '1', 8, 1, 1),    -- 9 unidades vendidas el 8 de enero de 2024
(9, 6, 90.00, '1', 9, 1, 1),     -- 6 unidades vendidas el 9 de enero de 2024
(10, 8, 120.00, '1', 10, 1, 1);  -- 8 unidades vendidas el 10 de enero de 2024


-- TABLA DETALLES

INSERT INTO detalles (ID_DETALLES, CANTIDAD, IMPORTE, IVA, ESTATUS, ID_PRODUCTO, ID_VENTA) VALUES
(1, 2, 30.00, 4.80, '1', 1, 1),   -- 2 unidades del producto 1 en la venta 1
(2, 1, 15.00, 2.40, '1', 2, 2),   -- 1 unidad del producto 2 en la venta 2
(3, 3, 45.00, 7.20, '1', 3, 3),   -- 3 unidades del producto 3 en la venta 3
(4, 5, 50.00, 8.00, '1', 4, 4),   -- 5 unidades del producto 4 en la venta 4
(5, 4, 46.00, 7.36, '1', 5, 5),   -- 4 unidades del producto 5 en la venta 5
(6, 2, 26.00, 4.16, '1', 6, 6),   -- 2 unidades del producto 6 en la venta 6
(7, 1, 14.50, 2.32, '1', 7, 7),   -- 1 unidad del producto 7 en la venta 7
(8, 3, 27.00, 4.32, '1', 8, 8),   -- 3 unidades del producto 8 en la venta 8
(9, 6, 90.00, 14.40, '1', 9, 9),   -- 6 unidades del producto 9 en la venta 9
(10, 4, 48.00, 7.68, '1', 10, 10); -- 4 unidades del producto 10 en la venta 10


-- TABLA ALMACEN

-- Almacén ajustado con ID_INTERMEDIARIO
INSERT INTO almacen (ID_PRODUCTO, NOMBRE, PRECIO_UNITARIO, EXISTENCIAS, PRECIO_EXISTENCIA, ESTATUS, ID_INTERMEDIARIO) VALUES
(1, 'Refresco Coca-Cola 600ml', 15.00, 100, 1500, '1', 1), -- Proveedor: Coca-Cola, Intermediario: 1
(2, 'Galletas María', 12.00, 80, 960, '1', 2), -- Proveedor: Galletas Donde, Intermediario: 2
(3, 'Huevos Grandes', 40.00, 30, 1200, '1', 3), -- Proveedor: Huevo Crio, Intermediario: 3
(4, 'Papitas La Lupita', 10.00, 50, 500, '0', 4), -- Proveedor: Botanas La Lupita, Intermediario: 4
(5, 'Sabritas Original 30g', 11.50, 120, 1380, '1', 5), -- Proveedor: Sabritas, Intermediario: 5
(6, 'Ruffles Queso 55g', 13.00, 60, 780, '0', 6), -- Proveedor: Barcel, Intermediario: 6
(7, 'Pepsi 600ml', 14.50, 90, 1305, '1', 7), -- Proveedor: Pepsi S.A.C, Intermediario: 7
(8, 'Chicharrones Los Compadres', 8.50, 45, 382.5, '0', 8), -- Proveedor: Botanas Los Compadres, Intermediario: 8
(9, 'Frituras Leo Picante', 9.00, 70, 630, '1', 9), -- Proveedor: Frituras Leo, Intermediario: 9
(10, 'Galletas Gamesa Marias', 10.00, 150, 1500, '1', 10), -- Proveedor: Gamesa, Intermediario: 10
(11, 'Huevos Crio Medianos', 38.00, 25, 950, '1', 3), -- Proveedor: Huevo Crio, Intermediario: 3
(12, 'Refresco Pepsi 2L', 30.00, 40, 1200, '1', 7), -- Proveedor: Pepsi S.A.C, Intermediario: 7
(13, 'Pan Molido Donde', 16.00, 50, 800, '1', 2), -- Proveedor: Galletas Donde, Intermediario: 2
(14, 'Refresco Coca-Cola 2L', 30.00, 60, 1800, '1', 1), -- Proveedor: Coca-Cola, Intermediario: 1
(15, 'Frituras Leo Sal', 10.00, 80, 800, '1', 9), -- Proveedor: Frituras Leo, Intermediario: 9
(16, 'Chetos Barcel', 15.00, 45, 675, '0', 6), -- Proveedor: Barcel, Intermediario: 6
(17, 'Sabritas Adobadas 30g', 11.50, 70, 805, '1', 5), -- Proveedor: Sabritas, Intermediario: 5
(18, 'Botanas La Lupita Picante', 9.50, 55, 522.5, '0', 4), -- Proveedor: Botanas La Lupita, Intermediario: 4
(19, 'Coca-Cola Sin Azúcar 600ml', 15.50, 65, 1007.5, '1', 1), -- Proveedor: Coca-Cola, Intermediario: 1
(20, 'Pan Dulce Gamesa', 18.00, 35, 630, '1', 10); -- Proveedor: Gamesa, Intermediario: 10


-- INTERMEDARIOS Y PROVEEDOR
INSERT INTO intermediario (ID_INTERMEDIARIO, NOMBRE, AP_MAT, AP_PAT, TEL, ESTATUS, ID_COMPANIA) VALUES
(1, 'Carlos', 'García', 'Pérez', '5551234874', 1, 1),
(2, 'Mariana', 'López', 'Hernández', '5555678765', 1, 2),
(3, 'José', 'Ramírez', 'Gutiérrez', '5552328765', 0, 3),
(4, 'Ana', 'Sánchez', 'Torres', '5558134321', 1, 4),
(5, 'David', 'Herrera', 'Ruiz', '5550922345', 0, 5),
(6, 'Sofía', 'Martínez', 'Domínguez', '5550289876', 1, 6),
(7, 'Luis', 'Vargas', 'Morales', '5552346543', 1, 7),
(8, 'Fernanda', 'Cruz', 'Castillo', '5555678769', 0, 8),
(9, 'Alejandro', 'Rivas', 'Jiménez', '5551233456', 1, 9),
(10, 'Gabriela', 'Muñoz', 'Salinas', '5552346789', 0, 10);

-- PRIMERO PROVEEDOR

INSERT INTO proveedor (ID_COMPANIA, NOMBRE, ESTATUS) VALUES
(1, 'Coca-cola ', 1),
(2, 'Galletas Donde', 1),
(3, 'Huevo Crio', 1),
(4, 'Botanas la lupita', 0),
(5, 'Sabritas', 1),
(6, 'Barcel', 0),
(7, 'Pepsi S.A.C', 1),
(8, 'Botonas lo compadres', 0),
(9, 'Frituras Leo', 1),
(10, 'Gamesa', 1);


