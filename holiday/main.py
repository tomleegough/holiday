from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from holiday.auth import login_required
import holiday.db_queries as db_queries

import icalendar

bp = Blueprint('main', __name__)

# TODO: Create activity view-only, not + edit
# TODO: Move activity/transport/accomodation delete to edit view
# TODO: Better sign up process, like Hermes
# TODO: Invite friends to trips
# TODO: Archive trips / Hide trips after end date


@bp.route('/')
@login_required
def index():

    return render_template(
        'holiday/index.html',
        trips=db_queries.get_all_current_trips(),
        view=''
    )

@bp.route('/hidden_trips')
@login_required
def hidden():
    return render_template(
        'holiday/index.html',
        trips=db_queries.get_all_trips(),
        view='hidden'
    )

@bp.route('/trip/create/', methods=['POST', 'GET'])
@login_required
def create_trip():
    if request.method == 'POST':
        db_queries.create_trip(request.form)

        return redirect(
            url_for(
                'main.index'
            )
        )

    return render_template(
        'forms/trip.html',
        trip='',
        action='add'
    )

@bp.route('/trip/<action>/<trip_id>', methods=['POST', 'GET'])
@login_required
def trip(action, trip_id):

    if action == 'view':

        return render_template(
            'holiday/trip-details-cards.html',
            trip=db_queries.get_one_trip(trip_id),
            accom=db_queries.get_trip_accommodation(trip_id),
            trans=db_queries.get_trip_transport(trip_id),
            activities=db_queries.get_trip_activities(trip_id)
        )

    if action == 'edit':
        if request.method == 'POST':

            db_queries.update_trip(request.form, trip_id)

            return redirect(
                url_for(
                    'main.trip',
                    action='view',
                    trip_id=trip_id
                )
            )

        return render_template(
            'forms/trip.html',
            trip=db_queries.get_one_trip(trip_id)
        )
    if action == 'delete':
            db_queries.delete_trip(trip_id)

            return redirect(
                url_for('main.index')
            )

    if action == 'archive':
        db_queries.archive_trip(trip_id)

        return redirect(
            url_for(
                'main.index'
            )
        )

    if action == 'unarchive':
        db_queries.unarchive_trip(trip_id)

        return redirect(
            url_for(
                'main.index'
            )
        )

    return render_template(
        'forms/trip.html',
        trip=db_queries.get_one_trip(trip_id),
        action=action
    )


@bp.route('/<trip_id>/<action>/<section>/', methods=['GET', 'POST'], defaults={'section_id': ''})
@bp.route('/<trip_id>/<action>/<section>/<section_id>', methods=['GET', 'POST'])
@login_required
def trip_info(trip_id, section, action, section_id):

    if section == 'transport':
        if action == 'add':
            if request.method == 'POST':

                db_queries.create_transport(request.form, trip_id)
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
                trip=db_queries.get_one_trip(trip_id)
            )

        if action == 'edit':
            if request.method == 'POST':
                db_queries.update_transport(request.form, section_id)
                return redirect(
                    url_for(
                        'main.trip',
                        action='view',
                        trip_id=trip_id
                    )
                )

            return render_template(
                'forms/transport.html',
                trans=db_queries.get_transport(section_id)
            )

        if action == 'delete':
            db_queries.delete_transport(section_id)

            return redirect(
                url_for(
                    'main.trip',
                    action='view',
                    trip_id=trip_id
                )
            )

    if section == 'accommodation':
        if action == 'add':
            if request.method == 'POST':
                db_queries.create_accomodation(request.form, trip_id)

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
                trip=db_queries.get_one_trip(trip_id),
                accom=''
            )

        if action == 'edit':
            if request.method == 'POST':
                db_queries.update_accomodation(request.form, section_id)

                return redirect(
                    url_for(
                        'main.trip',
                        action='view',
                        trip_id=trip_id
                    )
                )

            return render_template(
                'forms/accommodation.html',
                trip=db_queries.get_one_trip(trip_id),
                accom=db_queries.get_accomodation(section_id)
            )

        if action == 'delete':

            db_queries.delete_accomodation(section_id)

            return redirect(
                url_for(
                    'main.trip',
                    action='view',
                    trip_id=trip_id
                )
            )

    if section == 'activities':
        if action == 'add':
            if request.method == 'POST':

                db_queries.create_activity(request.data, trip_id)

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
                trip=db_queries.get_one_trip(trip_id)
            )

        if action == 'edit':
            if request.method == 'POST':
                db_queries.update_activity(request.form, section_id)
                return redirect(
                    url_for(
                        'main.trip',
                        action='view',
                        trip_id=trip_id
                    )
                )

            return render_template(
                'forms/activity.html',
                activity=db_queries.get_activity(section_id)
            )

        if action == 'delete':
            db_queries.delete_activity(activity_id)

            return redirect(
                url_for(
                    'main.trip',
                    action='view',
                    trip_id=trip_id
                )
            )

@bp.route('/calendar')
@login_required
# TODO: Make calendar secure
# TODO: Make calendar subscribable
def calendar():

    cal = icalendar.Calendar()
    cal.add('prodid', '-//tripper//tlg-accounting.co.uk')
    cal.add('version', '2.0')

    trips = db_queries.get_all_trips()

    for trip in trips:
        event = icalendar.Event()
        event['uid'] = trip['trip_id']
        event.add('Summary', trip['trip_name'])
        event.add('dtstart', trip['trip_start'])
        event.add('dtend', trip['trip_end'])
        cal.add_component(event)

    return cal.to_ical()

