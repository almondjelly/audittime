from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from model import GoogleCalendar, db, connect_to_db
import datetime


def get_last_7_days():
    """Use Google Calendar API to grab all calendar events over the last 7
    days that aren't already in the database."""

    # Set up the Calendar API
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow()
    now_text = now.isoformat() + 'Z'
    week_ago = now - datetime.timedelta(days=7)
    week_ago = week_ago.isoformat() + 'Z' # 'Z' indicates UTC time

    print('Getting all events over the last 7 days')
    events_result = service.events().list(calendarId='primary',
                                          timeMin=week_ago,
                                          timeMax=now_text,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    gcal_events = []

    # If calendar events exist, store them in gcal_events
    if events:
        for event in events:

            # If calendar event isn't in the database yet
            if GoogleCalendar.query.filter_by(gcal_event_id=event['id']).all(
               ) == []:

                gcal_event = {}

                # If the event is not an all day event, grab it
                if event['end'].get('dateTime'):
                    gcal_event['end'] = event['end'].get('dateTime')
                    gcal_event['start'] = event['start'].get('dateTime')
                    gcal_event['title'] = event['summary']
                    gcal_event['gcal_event_id'] = event['id']

                    gcal_events.append(gcal_event)

    return gcal_events


def update_db(user_id):
    """Add newly imported calendar events into the database."""

    gcal_events = get_last_7_days()

    for event in gcal_events:
        new_event = GoogleCalendar(gcal_event_id=event['gcal_event_id'],
                                   user_id=user_id,
                                   start_time=event['start'],
                                   stop_time=event['end'],
                                   title=event['title'],
                                   status='pending')
        db.session.add(new_event)

    db.session.commit()

    return


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
