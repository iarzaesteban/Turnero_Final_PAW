from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import google.auth

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'json_google/credential.json'

def get_google_calendar_events():
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
            creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE)

    # Si no hay credenciales válidas disponibles, solicita al usuario que inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Guarda las credenciales para la próxima ejecución.
        with open(CREDENTIALS_FILE, 'w') as token:
            token.write(creds.to_json())

    # Configura la API de Google Calendar.
    service = build('calendar', 'v3', credentials=creds)

    # Obtén los eventos del calendario del usuario.
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indica tiempo UTC.
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events

def solicitud_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()

            # Obtén los eventos del calendario al solicitar el turno.
            google_calendar_events = get_google_calendar_events()

            # Renderiza la página con los eventos del calendario.
            return render(request, 'turnos/solicitud_turno.html', {'form': form, 'events': google_calendar_events})
    else:
        form = TurnoForm()

    return render(request, 'turnos/solicitud_turno.html', {'form': form})