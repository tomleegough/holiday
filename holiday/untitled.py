@bp.route('/<trip_id>/<action>/<section>/', defaults={'section_id':''})
@bp.route('/<trip_id>/<action>/<section>/<section_id>', methods=['GET', 'POST'])
@login_required
def trip_info(trip, section, action, section_id):
    if section == 'transport':
        if action == 'add':
            if request.method == 'POST':
                transport_id = str(uuid.uuid4())
                transport_name = request.form['transport_name']
                transport_url = request.form['transport_url']
                transport_start = request.form['transport_start']
                transport_type = request.form['transport_type']
                transport_end = request.form['transport_end']
                transport_dur = request.form['transport_dur']
                transport_ref = request.form['transport_ref']
                transport_booking = request.form['transport_booking']
                transport_paid = request.form['transport_paid']
                db.execute(
                    'INSERT INTO transport ('
                    ' transport_id, transport_name, transport_url, transport_start,'
                    ' transport_end, transport_dur, transport_ref, transport_booking,'
                    ' transport_paid, transport_type, trip_id_fk)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (transport_id, transport_name, transport_url, transport_start,
                        transport_end, transport_dur, transport_ref, transport_booking,
                        transport_paid, transport_type, trip_id,)
                )

                db.commit()
                return redirect(url_for('main.trip', trip_id=trip_id))

            trip= db.execute(
                'SELECT * FROM trip WHERE trip_id = ?',
                (trip_id,)
            ).fetchone()
            return render_template('forms/transport.html', trip=trip)

        if action == 'edit':
            if request.method == 'POST':
                transport_name = request.form['transport_name']
                transport_url = request.form['transport_url']
                transport_start = request.form['transport_start']
                transport_type = request.form['transport_type']
                transport_dur = request.form['transport_dur']
                transport_ref = request.form['transport_ref']
                transport_booking = request.form['transport_booking']
                transport_paid = request.form['transport_paid']
                db.execute(
                    'UPDATE transport'
                    ' SET transport_name =?, transport_url=?,'
                    ' transport_start=?,transport_type=?,'
                    ' transport_dur=?, transport_ref=?,'
                    ' transport_booking=?, transport_paid=?',
                    ' WHERE transport_id=?',
                    (transport_name, transport_url, transport_start,
                        transport_end, transport_dur, transport_ref,
                        transport_booking, transport_paid, transport_type,
                        transport_id,)
                )
                db.commit()
                return redirect(url_for('main.trip', trip_id=trip_id))

            transport = db.execute(
                'SELECT * FROM transport WHERE trans_id=?',
                (trip_id,)
            ).fetchone()
            return render_template('forms/transport.html', trip=trip)

    if section == 'accomodation':