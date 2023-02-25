from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddSectionForm, EmptyForm, AddGuestForm
from app.forms import selectRoleForm, selectSectionForm, selectNameForm, editSocialLinksForm
from app.forms import nameOther
from app.models import User, Guest, Section


# TODO:
# make public/id
# to be public 
# Add link to user profile to see their public profile
# and keep private via link visibility
# ie: if guest has email, then show name with link. Else, don't.
# make reconnect page on the back of it - with the filter to sections

# TODO: Edit profiles for Admins

# TODO: Create an error page for when the app crashes. A 404 page will also be required

#
# PAGES
#

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

#
# LOGIN
#

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

#
# USER PRIVATE
#

@app.route('/user/<userid>', methods=['GET'])
@login_required
def user(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    guest = Guest.query.filter_by(email=user.email).first()
    if user.name:
        if user.id == current_user.id :
            return render_template('profile.html', user=user, userid=userid, guestid = guest.id)
        else:
            flash("You don't have permission to access this profile.")
            return redirect(url_for('user', userid=userid))      
    elif guest is None:
        flash('Take a few seconds to complete your profile.')
        return redirect(url_for('selectrole', userid=current_user.id))        
    
@app.route('/edit/role/<userid>', methods=['GET', 'POST'])
@login_required
def selectrole(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = selectRoleForm()
    if user.id == current_user.id :
        if form.validate_on_submit():
            if user.role == "admin":
                #TODO: Fix this - make it update the right user when admin
                return redirect(url_for('selectsection', userid=userid))
            else:
                user.role = form.roleselect.data
                db.session.commit()
                if user.role == "I graduated in 2005":
                    return redirect(url_for('selectsection', userid=current_user.id))
                elif user.role == "I was friends with people who graduated in 2005":
                    return redirect(url_for('nameother', userid=current_user.id))
                elif user.role == "I was a teacher at the EEB2":
                    return redirect(url_for('nameother', userid=current_user.id))
                elif user.role == "Other":
                    return redirect(url_for('nameother', userid=current_user.id))
                return redirect(url_for('user', userid=current_user.id))
        elif request.method == 'GET':
            form.roleselect.data = current_user.role
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=userid))
    return render_template('select-role.html', user=user, form=form)

@app.route('/edit/section/<userid>', methods=['GET', 'POST'])
@login_required
def selectsection(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = selectSectionForm()
    if user.id == current_user.id :
        if form.validate_on_submit():
            user.section = form.sectionselect.data
            db.session.commit()
            return redirect(url_for('nameselection', userid=userid))
        elif request.method == 'GET':
            form.sectionselect.data = current_user.section
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('select-section.html', user=user, form=form)

@app.route('/edit/name/<userid>', methods=['GET', 'POST'])
@login_required
def nameselection(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    currentsection = current_user.section
    form = selectNameForm(currentsection)
    if user.id == current_user.id :
        if form.validate_on_submit():
            user.name = form.nameselect.data
            guest = Guest.query.filter_by(name=user.name).first_or_404()
            guest.email = current_user.email
            guest.registered = 'yes'
            db.session.commit()
            return redirect(url_for('user', userid=userid))
        elif request.method == 'GET':
            form.nameselect.data = current_user.name
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=userid))
    return render_template('select-user.html', user=user, form=form)

@app.route('/edit/other/<userid>', methods=['GET', 'POST'])
@login_required
def nameother(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = nameOther()
    if user.id == current_user.id :
        if form.validate_on_submit():
            user.name = form.name.data
            db.session.commit()
            return redirect(url_for('user', userid=current_user.id))
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=userid))
    return render_template('name-other.html', user=user, form=form)

@app.route('/edit/social/<userid>', methods=['GET', 'POST'])
@login_required
def socialLinks(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = editSocialLinksForm()
    if user.id == current_user.id :
        if form.validate_on_submit():
            user.facebook = form.facebook.data
            user.twitter = form.twitter.data
            user.instagram = form.instagram.data
            user.linkedin = form.linkedin.data
            user.snapchat = form.snapchat.data
            user.reddit = form.reddit.data
            user.mastodon = form.mastodon.data
            user.tiktok = form.tiktok.data
            db.session.commit()
            return redirect(url_for('user', userid=userid))
        elif request.method == 'GET':
            form.facebook.data = current_user.facebook
            form.twitter.data = current_user.twitter
            form.instagram.data = current_user.instagram
            form.linkedin.data = current_user.linkedin
            form.snapchat.data = current_user.snapchat
            form.reddit.data = current_user.reddit
            form.mastodon.data = current_user.mastodon
            form.tiktok.data = current_user.tiktok
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('edit-social.html', user=user, form=form)

@app.route('/edit/reset/<userid>', methods=['GET','POST'])
@login_required
def resetProfile(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    guestToReset= Guest.query.filter_by(email=user.email).first()
    form = EmptyForm()
    if user.id == current_user.id :
        user.name = ''
        user.section = ''
        user.rsvp = 'Not yet'
        if user.role != 'admin':
            user.role = ''   
        if guestToReset: 
            guestToReset.email = None
            guestToReset.registered = 'no'
            guestToReset.rsvp = 'no'
        user.facebook = ''
        user.twitter = ''
        user.instagram = ''
        user.linkedin = ''
        user.snapchat = ''
        user.reddit = ''
        user.mastodon = ''
        user.tiktok = ''
        db.session.commit()
        if current_user.id == 'admin':
            return redirect(url_for('adminusermanagement'))
        else:
            return redirect(url_for('user', userid=current_user.id))
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    # return redirect(url_for('user', userid=userid))

#
# PUBLIC
# 

@app.route('/public/<guestid>', methods=['GET'])
@login_required
def public(guestid):
    guest = Guest.query.filter_by(id=guestid).first()
    user = User.query.filter_by(email=guest.email).first()

    return render_template('public.html', guestid=guestid, user=user)

@app.route('/reconnect', methods=['GET'])
@login_required
def reconnect():
    guests = Guest.query.order_by(Guest.section.asc())

    return render_template('reconnect.html', guests=guests)

#
# ADMIN
#

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

@app.route('/admin/guests', methods=['GET', 'POST'])
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

@app.route('/admin/delete/guest/<guestid>', methods=['GET', 'POST'])
@login_required
def delete_guest(guestid):
    currentguest = Guest.query.filter_by(id=guestid).first_or_404()
    if current_user.role == 'admin':
        db.session.delete(currentguest)
        # TODO: If guest is deleted, user with the name associated needs to be reset
        #       ie: you want to avoid having a user with the name of a deleted guest.
        db.session.commit()
        flash('Guest was deleted.')
        return redirect(url_for('adminguestmanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))