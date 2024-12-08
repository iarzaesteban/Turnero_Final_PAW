# Turnero_Final_PAW
Sistema de geston de turnos AR unlu

## Descripción del Proyecto: 
Hemos desarrollado un sistema de turnero para la Autoridad de Registro de la Universidad Nacional de Luján (UNLu) utilizando tecnologías modernas y robustas para garantizar su eficiencia, escalabilidad y seguridad. Este sistema está diseñado para facilitar la gestión de turnos de manera ágil y confiable, optimizando los procesos administrativos y mejorando la experiencia de los usuarios.

## Tecnologías Utilizadas:
### Backend:
- Django: Utilizamos Django como framework de desarrollo para el backend debido a su robustez, escalabilidad y capacidad de manejar aplicaciones complejas de manera eficiente.
### Frontend:
- HTML, CSS y JavaScript: La interfaz de usuario del sistema de turnos está desarrollada utilizando HTML para la estructura del contenido, CSS para el diseño y estilización, y JavaScript para la interacción dinámica y mejoras en la experiencia del usuario.
### Contenedores:
- Docker: Para garantizar que todos los servicios del sistema se ejecuten de manera consistente y aislada, utilizamos Docker. Docker nos permite empaquetar todas las dependencias y configuraciones necesarias en contenedores, facilitando la implementación y gestión del sistema.
### Base de Datos:
- PostgreSQL: Para el almacenamiento y gestión de datos.
### Control de Versiones:
- Git: Para el control de versiones y desarrollo del proyecto, utilizamos un repositorio Git. Esto nos permite gestionar cambios en el código de manera organizada, realizar seguimientos de versiones.
### Seguridad:
- ReCAPTCHA v3: Para asegurar la autenticidad de los usuarios y proteger el sistema contra accesos no autorizados y bots, implementamos ReCAPTCHA v3 en el proceso de inicio de sesión.
- Token CSRF: Utilizamos tokens CSRF (Cross-Site Request Forgery) para proteger todas las solicitudes POST, PUT, DELETE, previniendo así ataques que intenten realizar acciones no autorizadas en nombre del usuario autenticado.
- Encriptación de contraseñas: Las contraseñas de los usuarios se almacenan en la base de datos utilizando técnicas de encriptación para asegurar que no sean accesibles en texto plano, incrementando la seguridad de la información sensible.
- ORM de Django: Utilizamos el ORM (Object-Relational Mapping) de Django para interactuar con la base de datos, lo que nos permite realizar consultas y operaciones de manera segura, evitando inyecciones SQL y mejorando la integridad de los datos.
- Autenticación: Implementamos un sistema de autenticación robusto utilizando el middleware de autenticación de Django, que maneja la creación y manejo de sesiones de usuario de manera segura.
- Sesiones: Las sesiones de usuario se manejan mediante el middleware de sesiones de Django, con configuraciones que aseguran que las sesiones expiren después de una hora de inactividad y al cerrar el navegador.

### Funcionalidades Operadores:
- El sistema cuenta con un sistema de login.
- El sistema brindará la posibilidad de poder crear usuarios, para ello existe un mail de administración, que al crear un usuario, se enviará a dicho mail un código que te solicitará la web para poder crear el usuario y de esta forma evitar que cualquier persona cree un usuario.
- El sistema permitirá a los operadores logueados aceptar los turnos, cancelarlos o finalizarlos.
- Cuando el operador acepte un turno se le enviará al solicitante del turno un mail, indicando que se le aceptó el turno con una url que le permitirá cancelar el turno y un código para ingresarlo en la web y recordar los datos del turno. En el caso de que el operador cancele el turno, el sistema lo colocará nuevamente como disponible (al turno) y al solicitante, también, se le enviará un mail indicando dicho acontecimiento y la url para que pueda ingresar y solicitar un nuevo turno si así lo desea.
- Luego de haber atendido al solicitante del turno, el operador podrá marcar el turno como finalizado, siempre y cuando haya pasado el día y horario del mismo, no antes. 
- El sistema permitirá visualizar todos los turnos pendientes, además permitirá filtrar por aquellos turnos pendientes que sean para el día actual, y también filtrar por los turnos que se encuentren confirmados para el día actual.
- El sistema permitirá visualizar los turnos confirmados que tenga otro operador y además podrá autoasignarselo.
- El sistema permitirá visualizar los horarios de atención de los otros operadores que se encuentren cargados en el sistema.
- El sistema permitirá a los operadores enviar mail.
- El sistema permitirá visualizar reportes de los turnos, permitiendo filtrar por estado de los turnos, o por fecha desde y hasta, y además podrá exportarlo a un archivo excel.
- El sistema permitirá modificar el horario de atención de un usuario/operador, cambiar su contraseña, cambiar su avatar/foto, crear un nuevo usuario, gestionar el footer o pie de página (crear, editar o borrar una card) y cerrar sesión.  

### Funcionalidad del cliente:

- El sistema permitirá solicitar un turno, un cliente podrá tener máximo 2 turnos en estado pendiente.
- El sistema permitirá ingresar un código para que el cliente pueda recordar los datos de su turno.
- El sistema permitirá cancelar un turno, y en el caso de que el cliente desee dejar un comentario de porque lo canceló, podrá realizarlo.




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
9. Creamos un usuario:
    ```bash
    docker-compose exec web python3 manage.py createsuperuser
10. Ingresamos en el navegador:
   http://localhost:8000



### En el caso de no tener las keys para googleCalendar, por favor comiquese con el administrador para solicitarselas. Para que funciones correctamente posicionarse en la raíz del repositorio y ubicar dichas credenciales en: 
json_google/credential_keys.json
