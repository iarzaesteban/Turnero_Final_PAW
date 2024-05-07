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
9. Creamos un usuario:
    ```bash
    docker-compose exec web python3 manage.py createsuperuser
10. Ingresamos en el navegador:
   http://localhost:8000 o https://c62d-2800-af0-150a-bba2-1282-b2e1-bf6a-74ed.ngrok-free.app


En caso de que la url del último tip no funciones, ponerse en contacto con el desarrollador y solicitar la URL pertinente.


## Implementación

Contamos con dos tipos de usuarios:
* Operadores (cuentan con usuarios y gestionan los turnos)
* Clientes (no cuentan con usuario)

### Clientes
- Pueden solicitar un turno sin contar con un usuario.
- Pueden verificar el estado de su turno
- Pueden cancelar su turno (2 días previo al día del turno)
- No pueden contar con mas de dos turnos pendiente


### Operadores
- Puden visualizar turnos pendientes
- Pueden visualizar turnos pendientes y confirmados para el día actual
- Pueden visualizar un turno específico
- Pueden aceptar, cancelar, confirmar y finalizar un turno
- Pueden visualizar los turnos de otros operadores y asignarselos (si estan confirmados)
- Pueden enviar mails
- Pueden ver y emitir reportes
- Pueden modificar su propio horario de atención
- Pueden cambiar su contraseña
- Pueden cambiar su avatar/foto
- Pueden crear un usuario/operador
- Pueden Actualizar el pie de página
- Pueden cerrar sesion


### General
- Los turnos solo se pueden solicitar solo del mes actual hasta tres en adelante, por ejemplo si nos encotramos en enero, se podrá solicitar turno en enero, febrero o marzo.
- Los turnos solo se pueden solicitar cada 30 minutos.
- Si tengo un operador que atendie de 08:00AM a 17:00PM y otro de 09:00AM a 18:00PM por ejemplo, en el horario de las 08:00AM y 08:30AM solo se podrá haber un solo turno ya que solo se cuenta con un operador para atender esos horarios, en cambio en el horario de las 14:00hs, por ejemplo podra haber dos turnos, ya que tenemos a dos operadores para poder atender ambos turnos.
- El footer es dinámico, contamos con una sección dentro de la webapp para actualizar el footer.
- Si un cliente cancela un turno, se le enviará un mail al operador que tenia su turno para informarle de ello
- Si el operador, cancela o acepta un turno se envia un mail al cliente con lo sucedido y la información si desea canecelar el turno
- Los operadores en su primer login deberán cambiar la password y configurar sus horarios de atención
