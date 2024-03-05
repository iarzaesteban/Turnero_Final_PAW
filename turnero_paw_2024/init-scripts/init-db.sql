-- Nos conectamos a la base de datos
\c turnero_unlu;

-- Creamos la tabla Rol
CREATE TABLE Role (
    id_role SERIAL PRIMARY KEY,
    description VARCHAR(30) UNIQUE NOT NULL
);

-- Insertamos roles desde el archivo roles.csv
\COPY Role (description) FROM 'docker-entrypoint-initdb.d/csv/roles.csv' DELIMITER ',' CSV HEADER;


-- Creamos la tabla Persona
CREATE TABLE Person (
    id_person SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50)
);

-- Cargamos desde personas.csv la persona administradora
\COPY Person (first_name, last_name, email) FROM 'docker-entrypoint-initdb.d/csv/personas.csv' DELIMITER ',' CSV HEADER;


-- Creamos la tabla Usuario
CREATE TABLE Users (
    id_user SERIAL PRIMARY KEY,
    id_person INT REFERENCES Person(id_person),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    loggin BOOLEAN DEFAULT FALSE,
    start_time_attention DATE,
    end_time_attention DATE,
    picture BYTEA
);

-- Cargamos desde usuarios.csv el usuario administrador
\COPY Users (id_person, username, password_hash, loggin) FROM 'docker-entrypoint-initdb.d/csv/usuarios.csv' DELIMITER ',' CSV HEADER;

-- Creamos la tabla Estado
CREATE TABLE State (
    id_state SERIAL PRIMARY KEY,
    short_description VARCHAR(50),
    description VARCHAR(50)
);

\COPY State (short_description, description) FROM 'docker-entrypoint-initdb.d/csv/estados.csv' DELIMITER ',' CSV HEADER;

-- Creamos la tabla Turno
CREATE TABLE Shift (
    id_shift SERIAL PRIMARY KEY,
    date DATE,
    hour TIME,
    id_person INT REFERENCES Person(id_person),
    id_user INT REFERENCES Users(id_user) NULL,
    id_state INT REFERENCES State(id_state),
    confirmation_code VARCHAR(50),
    confirmation_url VARCHAR(255),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creamos la tabla Información Adicional
CREATE TABLE aditionalInformation(
    id_aditional_info SERIAL PRIMARY KEY,
    short_description VARCHAR(50),
    title VARCHAR(255),
    description TEXT,
    icon BYTEA
);

\COPY aditionalInformation (short_description, title, description, icon) FROM 'docker-entrypoint-initdb.d/csv/aditional_information.csv' DELIMITER ',' CSV HEADER;

-- Establecemos relaciones
ALTER TABLE Users ADD CONSTRAINT fk_user_person FOREIGN KEY (id_person) REFERENCES Person(id_person);
ALTER TABLE Shift ADD CONSTRAINT fk_shift_person FOREIGN KEY (id_person) REFERENCES Person(id_person);
ALTER TABLE Shift ADD CONSTRAINT fk_shift_user FOREIGN KEY (id_user) REFERENCES Users(id_user);
ALTER TABLE Shift ADD CONSTRAINT fk_shift_state FOREIGN KEY (id_state) REFERENCES State(id_state);