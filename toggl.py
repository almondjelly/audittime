from model import TogglEntry, db, connect_to_db
import datetime
from togglwrapper import Toggl


# Should ask for user's API token somewhere. This one's Gail's for testing.
toggl_api_token = 'f085fa351f1ac550e438cdc528ce1504'
toggl = Toggl(toggl_api_token)

now = datetime.datetime.utcnow()
now_text = now.isoformat() + 'Z'
week_ago = now - datetime.timedelta(days=7)
week_ago = week_ago.isoformat() + 'Z' # 'Z' indicates UTC time

entries = toggl.TimeEntries.get(start_date=week_ago)


def toggl_get_last_7_days():
    """Use Toggl API to grab all calendar events over the last 7
    days that aren't already in the database. Returns a list of toggl_entry
    objects."""

    now = datetime.datetime.utcnow()
    now_text = now.isoformat() + 'Z'
    week_ago = now - datetime.timedelta(days=7)
    week_ago = week_ago.isoformat() + 'Z' # 'Z' indicates UTC time

    print('Getting all events over the last 7 days')

    entries = toggl.TimeEntries.get(start_date=week_ago)

    toggl_entries = []

    for entry in entries:

        # If entry isn't in the database yet and the entry has a stop time
        if TogglEntry.query.filter_by(toggl_entry_id=entry['id']).all() == [] \
         and entry.get('stop'):

            toggl_entry = {}
            toggl_entry['title'] = entry.get('description', '(no description)')
            toggl_entry['toggl_entry_id'] = entry['id']
            toggl_entry['start'] = entry['start']
            toggl_entry['end'] = entry['stop']

            toggl_entries.append(toggl_entry)

    return toggl_entries


def toggl_update_db(user_id):
    """Add newly imported Toggl entries into the database."""

    toggl_entries = toggl_get_last_7_days()

    for entry in toggl_entries:
        new_entry = TogglEntry(toggl_entry_id=entry['toggl_entry_id'],
                               user_id=user_id,
                               start_time=entry['start'],
                               stop_time=entry['end'],
                               title=entry['title'],
                               status='pending')
        db.session.add(new_entry)

    db.session.commit()

    return


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
