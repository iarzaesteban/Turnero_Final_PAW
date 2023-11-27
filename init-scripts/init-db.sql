-- Nos conectamos a la base de datos
\c turnero_unlu;

-- Creamos la tabla Provincia
CREATE TABLE Provincia (
    id_provincia SERIAL PRIMARY KEY,
    nombre VARCHAR(30)
);

\COPY Provincia (nombre) FROM 'docker-entrypoint-initdb.d/csv/provincias.csv' DELIMITER ',' CSV HEADER;

-- Creamos la tabla Localidad
CREATE TABLE Localidad (
    id_localidad SERIAL PRIMARY KEY,
    nombre VARCHAR(30),
    id_provincia INT REFERENCES Provincia(id_provincia)
);

\COPY Localidad (nombre, id_provincia) FROM 'docker-entrypoint-initdb.d/csv/localidades.csv' DELIMITER ',' CSV HEADER;

-- Creamos la tabla Persona
CREATE TABLE Persona (
    id_persona SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    correo VARCHAR(50),
    telefono VARCHAR(15),
    dni VARCHAR(10),
    id_localidad INT REFERENCES Localidad(id_localidad)
);

-- Cargamos desde personas.csv la persona administradora
\COPY Persona (nombre, apellido, correo, telefono, dni, id_localidad) FROM 'docker-entrypoint-initdb.d/csv/personas.csv' DELIMITER ',' CSV HEADER;


-- Creamos la tabla Rol
CREATE TABLE Rol (
    id_rol SERIAL PRIMARY KEY,
    descripcion VARCHAR(30) UNIQUE NOT NULL
);

-- Insertamos roles desde el archivo roles.csv
\COPY Rol (descripcion) FROM 'docker-entrypoint-initdb.d/csv/roles.csv' DELIMITER ',' CSV HEADER;


-- Creamos la tabla Usuario
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    id_persona INT REFERENCES Persona(id_persona),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    loggin BOOLEAN DEFAULT FALSE,
    id_rol INT REFERENCES Rol(id_rol)
);

-- Cargamos desde usuarios.csv el usuario administrador
\COPY Usuario (id_persona, username, password_hash, loggin, id_rol) FROM 'docker-entrypoint-initdb.d/csv//usuarios.csv' DELIMITER ',' CSV HEADER;

-- Creamos la tabla Turno
CREATE TABLE Turno (
    id_turno SERIAL PRIMARY KEY,
    fecha DATE,
    hora TIME,
    estado VARCHAR(50)
);

-- Creamos la tabla Agente de Enrolamiento
CREATE TABLE AgenteDeEnrolamiento (
    id_agente SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES Usuario(id_usuario),
    horario_atencion VARCHAR(255),
    otros_atributos VARCHAR(255)
);

-- Establecemos relaciones
ALTER TABLE Usuario ADD CONSTRAINT fk_usuario_persona FOREIGN KEY (id_persona) REFERENCES Persona(id_persona);
ALTER TABLE AgenteDeEnrolamiento ADD CONSTRAINT fk_agente_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario);
