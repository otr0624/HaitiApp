from flask import Blueprint, render_template, flash, redirect, url_for
from app.patients.patient_model import PatientStatus
from app.settings.forms import PatientStatusForm
from app import db


settings_bp = Blueprint('settings_bp', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='assets')


@settings_bp.route('/')
def settings_home():
    list_obj = PatientStatus.query.all()
    form = PatientStatusForm(obj=list_obj)
    mode = "Settings"
    card_title = "Edit Custom Dropdowns"
    if form.validate_on_submit():
        list_obj.code_name = form.code_name.data
        list_obj.name = form.name.data
        db.session.add(list_obj)
        db.session.commit()
        flash("Patient status list successfully edited")
        return redirect(url_for('settings_bp.settings_home'))
    return render_template('settings-home-base.html', title="Settings",
                           mode=mode, card_title=card_title, list_obj=list_obj, form=form)
