from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddSectionForm, EmptyForm, AddGuestForm
from app.forms import selectRoleForm, selectSectionForm, selectNameForm
from app.models import User, Guest, Section

@app.route('/')
@app.route('/index')
def index():
    guestcount = Guest.query.count()
    usercount = Guest.query.filter_by(registered='yes').count()
    rsvpcount = Guest.query.filter_by(rsvp='yes').count()
    return render_template('index.html', title='Home',guestcount=guestcount, 
        usercount=usercount,rsvpcount=rsvpcount)

@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user',userid=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user',userid=current_user.id))
    return render_template('login.html', title='Sign In', form=form)

# TODO: Password reset functionality to build in

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
        user = User(username=form.email.data.lower(), name="", section="", email=form.email.data.lower(), role="",rsvp="Not yet")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<userid>')
@login_required
def user(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    if str(current_user.id) == str(userid):
        return render_template('profile.html', user=user)
    else:
        flash("You don't have permission to access this profile.")
        return redirect(url_for('user', userid=current_user.id))      

#   TODO: Add social links and make them editable

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

@app.route('/admin/delete-user/<userid>', methods=['GET', 'POST'])
@login_required
def delete_user(userid):
    usertodelete = User.query.filter_by(id=userid).first_or_404()
    if current_user.role == 'admin':
        if usertodelete.role == 'admin':
            flash('You can not delete an admin.')
        else:
            guestToClear = Guest.query.filter_by(email=usertodelete.email).first()
            if guestToClear is not None:

                guestToClear.email = None
                guestToClear.registered = 'no'
                guestToClear.rsvp = 'no'
            db.session.delete(usertodelete)
            db.session.commit()
            flash('User was deleted.')
            return redirect(url_for('adminusermanagement'))
        return redirect(url_for('adminusermanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))

#   TODO: Modify/Edit profile function by admins

@app.route('/admin/sections', methods=['GET'])
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

@app.route('/admin/delete-section/<sectionid>', methods=['GET', 'POST'])
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

@app.route('/admin/guests', methods=['GET'])
@login_required
def adminguestmanagement():
    if current_user.role == 'admin':
        guests = Guest.query.order_by(Guest.id.asc())
        form = AddGuestForm()
        if form.validate_on_submit():
            g = Guest(name=form.guestname.data.title(), section=form.section.data.upper(), registered="no", rsvp="no")
            gv = Guest.query.filter_by(name=g.name).first()
            if gv is not None:
                flash('Guest already exists')
                return redirect(url_for('adminguestmanagement'))
            else:
                db.session.add(g)
                db.session.commit()
                flash('Guest successfully added')
            return redirect(url_for('adminguestmanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))
    return render_template("guest_management.html", title='Guest list management', guests=guests, form=form)

#   TODO: Make it easy to clear guest email address
#         When this is been done, we need to clear the name from the relevant user. 
#
#         Similarly, we need to be able to clear the name off a guest and clear the 
#         email address from the guest. 

#   TODO: Make it easy for admins to edit guests. 

@app.route('/admin/delete-guest/<guestid>', methods=['GET', 'POST'])
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


@app.route('/edit-role/<userid>', methods=['GET', 'POST'])
@login_required
def selectrole(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = selectRoleForm()
    if str(current_user.id) == str(userid):
        if form.validate_on_submit():
            if user.role == "admin":
                return redirect(url_for('selectsection', userid=current_user.id))
            else:
                user.role = form.roleselect.data
                db.session.commit()
                if user.role == "I graduated in 2005":
                    return redirect(url_for('selectsection', userid=current_user.id))
                elif user.role == "I was friends with people who graduated in 2005":
                    return redirect(url_for('user', userid=current_user.id))
                    # TODO: Set a path for friends of graduates
                elif user.role == "I was a teacher at the EEB2":
                    #TODO: set a path for teachers
                    return redirect(url_for('user', userid=current_user.id))
                elif user.role == "Other":
                    # TODO: Set a path for Other
                    return redirect(url_for('user', userid=current_user.id))
                return redirect(url_for('user', userid=current_user.id))

# TODO: Reset the complete user form

# TODO: Create an error page for when the app crashes. A 404 page will also be 
#       required

    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('select-role.html', user=user, form=form)

@app.route('/edit-section/<userid>', methods=['GET', 'POST'])
@login_required
def selectsection(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = selectSectionForm()
    if str(current_user.id) == str(userid):
        if form.validate_on_submit():
            user.section = form.sectionselect.data
            db.session.commit()
            return redirect(url_for('nameselection', userid=current_user.id))
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('select-section.html', user=user, form=form)

@app.route('/edit-name/<userid>', methods=['GET', 'POST'])
@login_required
def nameselection(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    currentsection = current_user.section
    form = selectNameForm(currentsection)
    if str(current_user.id) == str(userid):
        if form.validate_on_submit():
            user.name = form.nameselect.data
            guest = Guest.query.filter_by(name=user.name).first_or_404()
            guest.email = current_user.email
            guest.registered = 'yes'
            db.session.commit()
            return redirect(url_for('user', userid=current_user.id))
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('select-user.html', user=user, form=form)

