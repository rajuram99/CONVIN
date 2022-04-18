from django.shortcuts import render
import os
import google_apis_oauth

from django.shortcuts import HttpResponseRedirect
import google_apis_oauth
from googleapiclient.discovery import build
from datetime import datetime

REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect'

SCOPES = ['https://www.googleapis.com/auth/calendar']

JSON_FILEPATH = os.path.join(os.getcwd(), 'client_id.json')

def GoogleCalendarInitView(request):
    oauth_url = google_apis_oauth.get_authorization_url(
        JSON_FILEPATH, SCOPES, REDIRECT_URI)
    return HttpResponseRedirect(oauth_url)
def home(request):
    return render(request, 'home.html')

def GoogleCalendarRedirectView(request):
    try:
        credentials = google_apis_oauth.get_crendentials_from_callback(
            request,
            JSON_FILEPATH,
            SCOPES,
            REDIRECT_URI
        )

        stringified_token = google_apis_oauth.stringify_credentials(credentials)
        creds, refreshed = google_apis_oauth.load_credentials(stringified_token)

        service = build('calendar', 'v3', credentials=creds)
        now = datetime.utcnow().isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    except Exception as e:
        print(e)
    return render(request, 'final.html', {"events" : events})