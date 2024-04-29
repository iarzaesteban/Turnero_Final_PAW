# Turnero_Final_PAW
Sistema de geston de turnos AR unlu

## Tecnilogías utilizadas:
- Python
- Django: Framework web utilizado en el backend.
- HTML, CSS y JavaScript: Utilizados para el frontend.


## Requerimientos
- Docker: Para la creación y gestión de contenedores.


## Instalación

1. Posiciónate en la raíz de tu directorio personal:
   ```bash
   cd ~

2. Clona el repositorio:
   ```bash
    git clone https://github.com/iarzaesteban/Turnero_Final_PAW.git
3. Ingresar al proyecto:
   ```bash
   cd Turnero_Final_PAW
4. Cambiamos branch:
   ```bash
   git checkout develop
5. Crea un enlace simbólico:
   ```bash
   sudo ln -s ~/Turnero_Final_PAW/turnero_paw_2024 /opt/turnero_paw_2024
6. Ingresamos al proyecto
   ```bash
   cd /opt/turnero_paw_2024
7. Levantamos el proyecto:
   ```bash
   docker-compose up
8. Abrimos otra terminal.
9. Corremos las migraciones
   ```bash
   docker-compose exec web python3 manage.py makemigrations
10. Corremos migrate:
    ```bashd
    docker-compose exec web python3 manage.py migrate
11. Cargamos la base de datos:
    ```bash
    docker-compose run --rm web python manage.py loaddata role
    docker-compose run --rm web python manage.py loaddata state
    docker-compose run --rm web python manage.py loaddata aditional_information
12. Creamos un usuario:
    ```bash
    docker-compose exec web python3 manage.py createsuperuser
14. Ingresamos en el navegador:
   http://localhost:8000



