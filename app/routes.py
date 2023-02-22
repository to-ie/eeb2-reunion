from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddSectionForm, EmptyForm, AddGuestForm
from app.models import User, Guest, Section


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/involved')
def involved():
    return render_template('get-involved.html', title='Get involved')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.email.data.lower(), email=form.email.data.lower(), role="user")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/admin/users', methods=['GET'])
@login_required
def adminusermanagement():
    if current_user.role == 'admin':
        users = User.query.order_by(User.id.asc())
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))
    return render_template("user_management.html", title='User management', 
        users=users)

@app.route('/admin/toggleadmin/<userid>', methods=['GET', 'POST'])
@login_required
def toggleadmin(userid):
    if current_user.role == 'admin':
        user = User.query.filter_by(id=userid).first()
        form = EmptyForm()
        if user.role == 'admin':
            if user.id == current_user.id:
                flash('You cannot remove your own admin rights.')
                return redirect(url_for('adminusermanagement'))
            else:
                user.role = ''
                db.session.commit()
                flash('Your changes have been saved: the user is no longer an \
                    admin.')
            return redirect(url_for('adminusermanagement'))
        else:
            user.role = 'admin'
            db.session.commit()
            flash('Your changes have been saved: the user is now an admin.')
            return redirect(url_for('adminusermanagement'))
        return redirect(url_for('adminusermanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))

@app.route('/admin/delete/user/<userid>', methods=['GET', 'POST'])
@login_required
def delete_user(userid):
    usertodelete = User.query.filter_by(id=userid).first_or_404()
    if current_user.role == 'admin':
        if usertodelete.role == 'admin':
            flash('You can not delete an admin.')
        else:
            db.session.delete(usertodelete)
            db.session.commit()
            flash('User was deleted.')
            return redirect(url_for('adminusermanagement'))
        return redirect(url_for('adminusermanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))


#
#       TODO:
#       Modify/Edit profiles by admins
#

@app.route('/admin/sections', methods=['GET', 'POST'])
@login_required
def adminsectionmanagement():
    if current_user.role == 'admin':
        sections = Section.query.order_by(Section.section.asc())
        form = AddSectionForm()
        if form.validate_on_submit():
            s = Section(section=form.sectioninput.data.upper())
            db.session.add(s)
            db.session.commit()
            flash('Section successfully added')
            return redirect(url_for('adminsectionmanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))
    return render_template("section_management.html", title='Section management', 
        sections=sections, form=form)


@app.route('/admin/delete/section/<sectionid>', methods=['GET', 'POST'])
@login_required
def delete_section(sectionid):
    currentsection = Section.query.filter_by(id=sectionid).first_or_404()
    if current_user.role == 'admin':
        db.session.delete(currentsection)
        db.session.commit()
        flash('Section was deleted.')
        return redirect(url_for('adminsectionmanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

# 
#       TODO: 
#       Style up the pages and error messages
# 

@app.route('/admin/guests', methods=['GET', 'POST'])
@login_required
def adminguestmanagement():
    if current_user.role == 'admin':
        guests = Guest.query.order_by(Guest.id.asc())
        form = AddGuestForm()
        if form.validate_on_submit():
            g = Guest(name=form.guestname.data.title(), section=form.section.data.upper())
            db.session.add(g)
            db.session.commit()
            flash('Guest successfully added')
            return redirect(url_for('adminguestmanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))
    return render_template("guest_management.html", title='Guest management', guests=guests, form=form)


@app.route('/admin/delete/guests/<guestid>', methods=['GET', 'POST'])
@login_required
def delete_guest(guestid):
    currentguest = Guest.query.filter_by(id=guestid).first_or_404()
    if current_user.role == 'admin':
        db.session.delete(currentguest)
        db.session.commit()
        flash('Guest was deleted.')
        return redirect(url_for('adminguestmanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))

#
# Guest list setup process:
# 1. Form to add a guest
#       - Section to be picked up from drop-down (db) 
# 2. List of guests added (as a table)
# 3. User to be able to update profile based on guest list 
#       - 'role' to be selected first (graduated, failed, teacher, other)
#       - 'section' to be selected if role = graduated
#       - 'name' and 'last name' to be picked, based on 'section' 
# 4. If first name, last name and section are selected, update guest list with 
#    email address and registered to be set as true
# 