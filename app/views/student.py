# from flask import Blueprint, render_template, flash, redirect, url_for, request
# from flask_login import login_required, current_user
# from app.forms.registration_to_studies import RegistrationtoStudiesForm
# from app.extensions import db
# from app.utils.decorators import admin_required


# bp = Blueprint('student', __name__)

# @bp.route('/registration_to_studies', methods=['GET', 'POST'])
# @login_required
# def registration_to_studies():
#     form = RegistrationtoStudiesForm()
#     if form.validate_on_submit():
#         studies =
#     return render_template("registration_to_studies", form=form)

# @bp.route('/studies_list', methods=['GET', 'POST'])
# @login_required
# def studies_list():
