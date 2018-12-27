from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from holiday.auth import login_required
from holiday.db import get_db

import uuid

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():

    db = get_db()

    trips = db.execute(
        'SELECT * FROM trip'
        ' WHERE user_id_fk=?'
        ' ORDER BY trip_start ASC',
        (session['user_id'],)
    ).fetchall()

    return render_template('holiday/index.html', trips=trips)


@bp.route('/trip/<action>/', methods=['POST', 'GET'], defaults={'trip_id': ''})
@bp.route('/trip/<action>/<trip_id>', methods=['POST', 'GET'])
@login_required
def trip(action, trip_id):
    db = get_db()
    trip_data = db.execute(
        'SELECT * FROM trip WHERE trip_id=? and user_id_fk=?',
        (trip_id, session['user_id'],)
    ).fetchone()

    if action == 'view':
        accommodation = db.execute(
            'SELECT * FROM accommodation'
            ' WHERE trip_id_fk = ?'
            ' ORDER BY accom_start asc, accom_time asc',
            (trip_id,)
        ).fetchall()

        transport = db.execute(
            'SELECT * FROM transport'
            ' WHERE trip_id_fk = ?'
            ' ORDER BY transport_start asc, transport_time asc',
            (trip_id,)
        ).fetchall()

        activities = db.execute(
            'SELECT *, ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS row_num'
            ' FROM activity'
            ' WHERE trip_id_fk = ?',
            (trip_id,)
        ).fetchall()

        return render_template(
            'holiday/trip-details-table.html',
            trip=trip_data,
            accom=accommodation,
            trans=transport,
            activities=activities
        )

    if action == 'add':
        if request.method == 'POST':
            trip_name = request.form['trip_name']
            trip_start = request.form['trip_start']
            trip_end = request.form['trip_end']
            if 'trip_accommodation' in request.form:
                trip_accommodation = 1
            else:
                trip_accommodation = 0
            if 'trip_transport' in request.form:
                trip_transport = 1
            else:
                trip_transport = 0
            if 'trip_activities' in request.form:
                trip_activities = 1
            else:
                trip_activities = 0
            db = get_db()
            db.execute(
                'INSERT INTO trip (trip_id, trip_name,'
                '  trip_start, trip_end, trip_accommodation,'
                '  trip_transport, trip_activities, user_id_fk)'
                ' VALUES'
                '  (?, ?, ?, ?, ?, ?, ?, ?)',
                (str(uuid.uuid4()), trip_name, trip_start,
                    trip_end, trip_accommodation,
                    trip_transport, trip_activities, session['user_id'])
            )
            db.commit()
            return redirect(url_for('main.index'))

        return render_template(
            'forms/trip.html',
            trip=trip,
            action=action
        )

    if action == 'edit':
        if request.method == 'POST':
            trip_name = request.form['trip_name']
            trip_start = request.form['trip_start']
            trip_end = request.form['trip_end']
            if 'trip_accommodation' in request.form:
                trip_accommodation = 1
            else:
                trip_accommodation = 0
            if 'trip_transport' in request.form:
                trip_transport = 1
            else:
                trip_transport = 0
            if 'trip_activities' in request.form:
                trip_activities = 1
            else:
                trip_activities = 0

            db.execute(
                'UPDATE trip'
                ' SET trip_name=?, trip_start=?,'
                '  trip_end=?, trip_accommodation=?,'
                '  trip_transport=?, trip_activities=?'
                ' WHERE trip_id=?',
                (trip_name, trip_start, trip_end,
                    trip_accommodation, trip_transport,
                    trip_activities, trip_id,)
            )
            db.commit()
            return redirect(
                url_for(
                    'main.trip',
                    action='view',
                    trip_id=trip_id
                )
            )

    return render_template('forms/trip.html', trip=trip_data, action=action)


@bp.route('/<trip_id>/<action>/<section>/', methods=['GET', 'POST'], defaults={'section_id': ''})
@bp.route('/<trip_id>/<action>/<section>/<section_id>', methods=['GET', 'POST'])
@login_required
def trip_info(trip_id, section, action, section_id):
    db = get_db()

    trip = db.execute(
        'SELECT * FROM trip WHERE trip_id = ? and user_id_fk = ?',
        (trip_id, session['user_id'], )
    ).fetchone()

    if section == 'transport':
        if action == 'add':
            if request.method == 'POST':
                transport_id = str(uuid.uuid4())
                transport_name = request.form['transport_name']
                transport_url = request.form['transport_url']
                transport_start = request.form['transport_start']
                transport_type = request.form['transport_type']
                transport_time = request.form['transport_time']
                transport_dur = request.form['transport_dur']
                transport_ref = request.form['transport_ref']
                transport_notes = request.form['transport_notes']
                transport_booking = request.form['transport_booking']
                transport_paid = request.form['transport_paid']
                db.execute(
                    'INSERT INTO transport ('
                    ' transport_id, transport_name, transport_url,'
                    ' transport_start, transport_dur,'
                    ' transport_ref, transport_booking,'
                    ' transport_paid, transport_type, transport_time,'
                    ' transport_notes, trip_id_fk)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (transport_id, transport_name, transport_url,
                        transport_start, transport_dur,
                        transport_ref, transport_booking,
                        transport_paid, transport_type, transport_time,
                        transport_notes, trip_id,)
                )

                db.commit()
                return redirect(
                    url_for(
                        'main.trip',
                        trip_id=trip_id,
                        action='view'
                    )
                )

            return render_template(
                'forms/transport.html',
                action=action,
                trans='',
                trip=trip
            )

        if action == 'edit':
            if request.method == 'POST':
                transport_name = request.form['transport_name']
                transport_url = request.form['transport_url']
                transport_start = request.form['transport_start']
                transport_time = request.form['transport_time']
                transport_type = request.form['transport_type']
                transport_dur = request.form['transport_dur']
                transport_notes = request.form['transport_notes']
                transport_ref = request.form['transport_ref']
                transport_booking = request.form['transport_booking']
                transport_paid = request.form['transport_paid']
                db.execute(
                    'UPDATE transport'
                    ' SET transport_name =?, transport_url=?,'
                    ' transport_start=?,transport_type=?,'
                    ' transport_dur=?, transport_ref=?,'
                    ' transport_booking=?, transport_paid=?,'
                    ' transport_time=?, transport_notes=?'
                    ' WHERE transport_id=?',
                    (transport_name, transport_url, transport_start,
                        transport_type, transport_dur, transport_ref,
                        transport_booking, transport_paid, transport_time,
                        transport_notes, section_id,)
                )
                db.commit()
                return redirect(
                    url_for(
                        'main.trip',
                        action='view',
                        trip_id=trip_id
                    )
                )

            transport = db.execute(
                'SELECT * FROM transport WHERE transport_id=?',
                (section_id,)
            ).fetchone()
            return render_template('forms/transport.html', trans=transport)

    if section == 'accommodation':
        if action == 'add':
            if request.method == 'POST':
                accom_id = str(uuid.uuid4())
                accom_start = request.form['accom_start']
                accom_end = request.form['accom_end']
                accom_name = request.form['accom_name']
                accom_url = request.form['accom_url']
                accom_address = request.form['accom_address']
                accom_postcode = request.form['accom_postcode']
                accom_booking = request.form['accom_booking']
                accom_paid = request.form['accom_paid']
                accom_time = request.form['accom_time']
                trip_id_fk = trip_id

                db.execute(
                    'INSERT INTO accommodation ('
                    ' accom_id, accom_start, accom_end, accom_name,'
                    ' accom_url, accom_address, accom_postcode, accom_time,'
                    '  trip_id_fk, accom_booking, accom_paid)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (accom_id, accom_start, accom_end, accom_name,
                        accom_url, accom_address, accom_postcode, accom_time,
                        trip_id_fk, accom_booking, accom_paid,)
                )

                db.commit()

                return redirect(
                    url_for(
                        'main.trip',
                        action='view',
                        trip_id=trip_id
                    )
                )

            return render_template(
                'forms/accommodation.html',
                action=action,
                trip=trip,
                accom=''
            )

        if action == 'edit':
            if request.method == 'POST':
                accom_id = section_id
                accom_start = request.form['accom_start']
                accom_end = request.form['accom_end']
                accom_name = request.form['accom_name']
                accom_url = request.form['accom_url']
                accom_address = request.form['accom_address']
                accom_postcode = request.form['accom_postcode']
                accom_booking = request.form['accom_booking']
                accom_paid = request.form['accom_paid']
                accom_time = request.form['accom_time']
                trip_id_fk = trip_id

                db.execute(
                    'UPDATE accommodation '
                    'SET accom_start=?, accom_end=?, accom_name=?,'
                    ' accom_url=?, accom_address=?, accom_postcode=?,'
                    ' accom_booking=?, accom_paid=?,'
                    ' trip_id_fk=?, accom_time=?'
                    ' WHERE accom_id=?',
                    (accom_start, accom_end, accom_name, accom_url,
                        accom_address, accom_postcode, accom_booking,
                        accom_paid, trip_id_fk, accom_time, accom_id)
                )

                db.commit()

                return redirect(
                    url_for(
                        'main.trip',
                        action='view',
                        trip_id=trip_id
                    )
                )

            accom = db.execute(
                'SELECT * FROM accommodation WHERE accom_id=?',
                (section_id,)
            ).fetchone()

            return render_template(
                'forms/accommodation.html', trip=trip, accom=accom
            )

    if section == 'activities':
        if action == 'add':
            if request.method == 'POST':
                activity_id = str(uuid.uuid4())
                activity_name = request.form['activity_name']
                activity_url = request.form['activity_url']
                activity_description = request.form['activity_description']
                activity_travel_time = request.form['activity_travel_time']
                activity_travel_method = request.form['activity_travel_method']
                activity_status = request.form['activity_status']

                db.execute(
                    'INSERT INTO activity ('
                    ' activity_id, activity_name, activity_url,'
                    ' activity_description, activity_travel_time, '
                    ' activity_travel_method, activity_status, trip_id_fk)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (activity_id, activity_name, activity_url,
                        activity_description, activity_travel_time,
                        activity_travel_method, activity_status, trip_id,)
                )

                db.commit()
                return redirect(
                    url_for(
                        'main.trip',
                        trip_id=trip_id,
                        action='view'
                    )
                )

            return render_template(
                'forms/activity.html',
                action=action,
                activity='',
                trip=trip
            )

        if action == 'edit':
            if request.method == 'POST':
                activity_id = str(uuid.uuid4())
                activity_name = request.form['activity_name']
                activity_url = request.form['activity_url']
                activity_description = request.form['activity_description']
                activity_travel_time = request.form['activity_travel_time']
                activity_travel_method = request.form['activity_travel_method']
                activity_status = request.form['activity_status']

                db.execute(
                    'UPDATE activity'
                    ' SET'
                    '  activity_name = ?,'
                    '  activity_url = ?,'
                    '  activity_description = ?,'
                    '  activity_travel_time = ?,'
                    '  activity_travel_method = ?,'
                    '  activity_status = ?,'
                    '  trip_id_fk = ?'
                    ' WHERE activity_id = ?',
                    (activity_name, activity_url, activity_description,
                        activity_travel_time, activity_travel_method,
                        activity_status, trip_id, section_id,)
                )
                db.commit()
                return redirect(
                    url_for(
                        'main.trip',
                        action='view',
                        trip_id=trip_id
                    )
                )

            activity = db.execute(
                'SELECT * FROM activity WHERE activity_id=?',
                (section_id,)
            ).fetchone()
            return render_template('forms/activity.html', activity=activity)
