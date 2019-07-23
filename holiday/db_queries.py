from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from holiday.db import get_db
from uuid import uuid4

bp = Blueprint('db_queries', __name__)

def get_all_trips():
    db = get_db()

    trips = db.execute(
        'SELECT * FROM trip'
        ' WHERE user_id_fk=?'
        ' ORDER BY trip_start ASC',
        (session['user_id'],)
    ).fetchall()

    return trips

def get_one_trip(trip_id):
    db = get_db()

    trip_data = db.execute(
        'SELECT * FROM trip WHERE trip_id=? and user_id_fk=?',
        (trip_id, session['user_id'],)
    ).fetchone()

    return trip_data

def get_trip_accommodation(trip_id):
    db = get_db()

    accommodation = db.execute(
        'SELECT * FROM accommodation'
        ' WHERE trip_id_fk = ?'
        ' ORDER BY accom_start asc, accom_time asc',
        (trip_id,)
    ).fetchall()

    return accommodation

def get_trip_transport(trip_id):
    db = get_db()

    transport = db.execute(
        'SELECT * FROM transport'
        ' WHERE trip_id_fk = ?'
        ' ORDER BY transport_start asc, transport_time asc',
        (trip_id,)
    ).fetchall()

    return transport

def get_trip_activities(trip_id):
    db = get_db()

    activities = db.execute(
        'SELECT *, ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS row_num'
        ' FROM activity'
        ' WHERE trip_id_fk = ?',
        (trip_id,)
    ).fetchall()

    return activities

def create_trip(form_data):
    db = get_db()

    if 'trip_accommodation' in form_data:
        trip_accommodation = 1
    else:
        trip_accommodation = 0
    if 'trip_transport' in form_data:
        trip_transport = 1
    else:
        trip_transport = 0
    if 'trip_activities' in form_data:
        trip_activities = 1
    else:
        trip_activities = 0

    db.execute(
        'INSERT INTO'
        ' trip ('
        '  trip_id,'
        '  trip_name,'
        '  trip_start,'
        '  trip_end,'
        '  trip_accommodation,'
        '  trip_transport,'
        '  trip_activities,'
        '  user_id_fk'
        ' ) VALUES ('
        '  ?,'
        '  ?,'
        '  ?,'
        '  ?,'
        '  ?,'
        '  ?,'
        '  ?,'
        '  ?'
        ' )',
        (
            str(uuid4()),
            form_data['trip_name'],
            form_data['trip_start'],
            form_data['trip_end'],
            trip_accommodation,
            trip_transport,
            trip_activities,
            session['user_id'],
        )
    )

    db.commit()

def update_trip(form_data, trip_id):
    db = get_db()

    if 'trip_accommodation' in form_data:
        trip_accommodation = 1
    else:
        trip_accommodation = 0
    if 'trip_transport' in form_data:
        trip_transport = 1
    else:
        trip_transport = 0
    if 'trip_activities' in form_data:
        trip_activities = 1
    else:
        trip_activities = 0

    db.execute(
        'UPDATE'
        '  trip'
        ' SET'
        '  trip_name=?,'
        '  trip_start=?,'
        '  trip_end=?,'
        '  trip_accommodation=?,'
        '  trip_transport=?,'
        '  trip_activities=?'
        ' WHERE'
        '  trip_id=?',
        (
            form_data['trip_name'],
            form_data['trip_start'],
            form_data['trip_end'],
            trip_accommodation,
            trip_transport,
            trip_activities,
            trip_id,
        )
    )
    db.commit()

def delete_trip(trip_id):
    db = get_db()

    db.execute(
        'DELETE FROM trip'
        ' WHERE trip_id = ?',
        (trip_id,)
    )

    db.execute(
        'DELETE FROM transport'
        ' WHERE trip_id_fk = ?',
        (trip_id,)
    )

    db.execute(
        'DELETE FROM accommodation'
        ' WHERE trip_id_fk = ?',
        (trip_id,)
    )

    db.execute(
        'DELETE FROM activity'
        ' WHERE trip_id_fk = ?',
        (trip_id,)
    )

    db.commit()

def create_transport(form_data, trip_id):
    db = get_db()

    db.execute(
        'INSERT INTO'
        ' transport ('
        '   transport_id,'
        '   transport_name,'
        '   transport_url,'
        '   transport_start,'
        '   transport_dur,'
        '   transport_ref,'
        '   transport_booking,'
        '   transport_paid,'
        '   transport_type,'
        '   transport_time,'
        '   transport_notes, '
        '   trip_id_fk'
        ') VALUES ('
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?)',
        (
            str(uuid4()),
            form_data['transport_name'],
            form_data['transport_url'],
            form_data['transport_start'],
            form_data['transport_dur'],
            form_data['transport_ref'],
            form_data['transport_booking'],
            form_data['transport_paid'],
            form_data['transport_type'],
            form_data['transport_time'],
            form_data['transport_notes'],
            trip_id,
        )
    )

    db.commit()


def update_transport(form_data, transport_id):
    db = get_db()

    db.execute(
        'UPDATE'
        '  transport'
        ' SET'
        '   transport_name =?,'
        '   transport_url=?,'
        '   transport_start=?,'
        '   transport_type=?,'
        '   transport_dur=?, '
        '   transport_ref=?,'
        '   transport_booking=?,'
        '   transport_paid=?,'
        '   transport_time=?,'
        '   transport_notes=?'
        ' WHERE'
        '   transport_id=?',
        (
            form_data['transport_name'],
            form_data['transport_url'],
            form_data['transport_start'],
            form_data['transport_type'],
            form_data['transport_dur'],
            form_data['transport_ref'],
            form_data['transport_booking'],
            form_data['transport_paid'],
            form_data['transport_time'],
            form_data['transport_notes'],
            transport_id,
        )
    )

    db.commit()

def get_transport(transport_id):
    db = get_db()

    transport = db.execute(
        'SELECT'
        '   *'
        ' FROM'
        '   transport'
        ' WHERE'
        '   transport_id=?',
        (
            transport_id
        )
    ).fetchone()

    return transport

def delete_transport(transport_id):
     db = get_db()

     db.execute(
         'DELETE FROM'
         '   transport'
         ' WHERE'
         '   transport_id = ?',
         (
             transport_id,
          )
     )

     db.commit()

def create_accomodation(form_data, trip_id):
    db = get_db()

    db.execute(
        'INSERT INTO'
        ' accommodation ('
        '   accom_id,'
        '   accom_start,'
        '   accom_end,'
        '   accom_name,'
        '   accom_url,'
        '   accom_address,'
        '   accom_postcode,'
        '   accom_time,'
        '   accom_booking,'
        '   accom_paid,'
        '   trip_id_fk'
        ' ) VALUES ('
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?)',
        (
            str(uuid4()),
            form_data['accom_start'],
            form_data['accom_end'],
            form_data['accom_name'],
            form_data['accom_url'],
            form_data['accom_address'],
            form_data['accom_postcode'],
            form_data['accom_time'],
            form_data['accom_booking'],
            form_data['accom_paid'],
            trip_id,
        )
    )

    db.commit()

def update_accomodation(form_data, accom_id):
    db = get_db()

    db.execute(
        'UPDATE'
        ' accommodation '
        'SET'
        '   accom_start=?,'
        '   accom_end=?,'
        '   accom_name=?,'
        '   accom_url=?,'
        '   accom_address=?,'
        '   accom_postcode=?,'
        '   accom_booking=?,'
        '   accom_paid=?,'
        '   accom_time=?'
        ' WHERE'
        '   accom_id=?',
        (
            form_data['accom_start'],
            form_data['accom_end'],
            form_data['accom_name'],
            form_data['accom_url'],
            form_data['accom_address'],
            form_data['accom_postcode'],
            form_data['accom_booking'],
            form_data['accom_paid'],
            form_data['accom_time'],
            accom_id,
        )
    )

    db.commit()


def get_accomodation(accom_id):
    db = get_db()

    accom = db.execute(
        'SELECT'
        '   *'
        ' FROM'
        '   accommodation'
        ' WHERE'
        '   accom_id=?',
        (
            accom_id
        )
    ).fetchone()

    return accom


def delete_accomodation(accom_id):
    db = get_db()

    db.execute(
        'DELETE FROM'
        '   accommodation'
        ' WHERE'
        '   accom_id = ?',
        (
            accom_id,
        )
    )

    db.commit()


def create_activity(form_data, trip_id):
    db = get_db()

    db.execute(
        'INSERT INTO'
        ' activity ('
        '   activity_id,'
        '   activity_name,'
        '   activity_url,'
        '   activity_description,'
        '   activity_travel_time, '
        '   activity_travel_method,'
        '   activity_status,'
        '   trip_id_fk'
        ' ) VALUES ('
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?,'
        '   ?'
        ' )',
        (
            str(uuid4()),
            form_data['activity_name'],
            form_data['activity_url'],
            form_data['activity_description'],
            form_data['activity_travel_time'],
            form_data['activity_travel_method'],
            form_data['activity_status'],
            trip_id,
        )
    )

    db.commit()


def update_activity(form_data, activity_id):
    db = get_db()

    db.execute(
        'UPDATE'
        '  activity'
        ' SET'
        '    activity_name = ?,'
        '    activity_url = ?,'
        '    activity_description = ?,'
        '    activity_travel_time = ?,'
        '    activity_travel_method = ?,'
        '    activity_status = ?'
        ' WHERE'
        '   activity_id = ?',
        (
            form_data['activity_name'],
            form_data['activity_url'],
            form_data['activity_description'],
            form_data['activity_travel_time'],
            form_data['activity_travel_method'],
            form_data['activity_status'],
            activity_id,
        )
    )
    db.commit()


def get_activity(activity_id):
    db = get_db()

    activity = db.execute(
        'SELECT'
        '   *'
        ' FROM'
        '   activity'
        ' WHERE'
        '   activity_id=?',
        (
            activity_id,
        )
    ).fetchone()

    return activity


def delete_activity(activity_id):
    db = get_db()

    db.execute(
        'DELETE FROM'
        '   activity'
        ' WHERE'
        '   activity_id = ?',
        (
            activity_id,
        )
    )

    db.commit()