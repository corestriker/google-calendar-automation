# Automate Google Calendar Event Creator

Creates Events to a give Google Calendar. So you can automate a reminder for bring out the trashcan.

This script will create an event one day before the give date at 5PM with a 15 minutes timeslot and a reminder 10 minutes before push (popup).

## Install

Install requirements:

```bash
 pip install -r requirements.txt
```

Copy events and env examples to local:

```bash
cp example.events.txt events.txt
cp example.env .env
```

Fill in your eventdates to `events.txt`
Fill in your Google Calender ID to `.env`

Use `list_calendars()` function to retrive available caledar ids
