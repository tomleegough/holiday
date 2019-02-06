from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from holiday.db import get_db

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