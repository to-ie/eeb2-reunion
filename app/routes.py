import os
import imghdr
from app import app, db
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request, abort, Response
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm, AddSectionForm, EmptyForm, AddGuestForm
from app.forms import selectRoleForm, selectSectionForm, selectNameForm, editSocialLinksForm
from app.forms import nameOther, ProfilePictureForm, selectLocationForm
from app.forms import ResetPasswordRequestForm, rsvpForm
from app.forms import ResetPasswordForm, contactForm, inviteForm
from app.models import User, Guest, Section
from flask_wtf.file import FileField
from app.email import send_password_reset_email, send_verification_email, send_contact_email
from app.email import send_invite_email, new_user_email, profile_reset_email
from app.email import new_rsvp_email


#
# PAGES ------------------------------------------------------------------------
#

@app.route('/')
@app.route('/index')
def index():
    guestcount = Guest.query.count()
    usercount = Guest.query.filter_by(registered='yes').count()
    rsvpcount = User.query.filter_by(rsvp='yes').count()
    return render_template('index.html', title='Home',guestcount=guestcount, 
        usercount=usercount, rsvpcount=rsvpcount)

@app.route('/about')
@login_required
def about():
    guestcount = Guest.query.count()
    usercount = Guest.query.filter_by(registered='yes').count()
    rsvpcount = User.query.filter_by(rsvp='yes').count()
    return render_template('about.html', title='About', guestcount=guestcount, 
        usercount=usercount,rsvpcount=rsvpcount)

#
# LOGIN ------------------------------------------------------------------------
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
        if user.verified != 'yes':
            flash('Please confirm your account. Check your inbox (or spam folder)\
                 for the verification email.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user',userid=current_user.id))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered.')
        return redirect(url_for('user', userid=current_user.id))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.email.data.lower(), name="", section="", 
                    email=form.email.data.lower(), 
            role="",rsvp="Not yet", currentlocation="", verified='no')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user, userid=user.id)
        new_user_email(user)
        return redirect(url_for('confirmation'))
    return render_template('register.html', title='Register', form=form)


@app.route('/confirmation', methods=['GET'])
def confirmation():
    return render_template('confirmation.html', title='Confirmation')


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('If the account exists, we have sent you the instructions to reset \
            your password. Check your emails.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/verify_request', methods=['GET', 'POST'])
def verify_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = EmptyForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        send_verification_email(user, userid=user.id)
        return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/verify/rRqzJgsWs5g3XQ5UDj<userid>', methods=['GET', 'POST'])
def verify_account(userid):
    if current_user.is_authenticated:
        return redirect(url_for('user', userid=current_user.id))
    user = User.query.filter_by(id=userid).first()
    if not user:
        return redirect(url_for('login'))
    user.verified = 'yes'
    db.session.commit()
    flash('Your account is now verified, you can login.')
    return redirect(url_for('login'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = contactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        captcha = form.captcha.data
        if captcha == '7' or captcha == 'seven' or captcha == 'Seven':
            send_contact_email(name=name, email=email, message=message, captcha=captcha)
            flash('Your message was sent.')
            return redirect(url_for('index'))
        flash('Check the captcha there?')
    return render_template('contact.html', form=form)


#
# USER PRIVATE -----------------------------------------------------------------
#

@app.route('/user/<userid>', methods=['GET'])
@login_required
def user(userid):
    user = User.query.filter_by(id=userid).first()
    guest = Guest.query.filter_by(email=user.email).first()
    if user.name:
        if guest is None and user.id == current_user.id:
            return render_template('profile.html', user=user, userid=userid)
        elif user.id == current_user.id :
            return render_template('profile.html', user=user, userid=userid, 
                guestid = guest.id)
        elif guest is None and current_user.role == 'admin':
            return render_template('profile.html', user=user, userid=userid)
        elif current_user.role == 'admin' :
            return render_template('profile.html', user=user, userid=userid, 
                guestid = guest.id)
        else:
            flash("You don't have permission to access this profile.")
            return redirect(url_for('user', userid=current_user.id))      
    elif guest is None:
        flash('Take a few seconds to complete your profile.')
        return redirect(url_for('selectrole', userid=userid))    

@app.route('/edit/role/<userid>', methods=['GET', 'POST'])
@login_required
def selectrole(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = selectRoleForm()
    if user.id == current_user.id or current_user.role=='admin':
        if form.validate_on_submit():
            if user.role == "admin":
                #TODO: Fix this - make it update the right user when admin
                return redirect(url_for('selectsection', userid=userid))
            else:
                user.role = form.roleselect.data
                db.session.commit()
                if user.role == "I graduated in 2005":
                    return redirect(url_for('selectsection', userid=userid))
                elif user.role == "I was friends with people who graduated in 2005":
                    return redirect(url_for('nameother', userid=userid))
                elif user.role == "I was a teacher at the EEB2":
                    return redirect(url_for('nameother', userid=userid))
                elif user.role == "Other":
                    return redirect(url_for('nameother', userid=userid))
                return redirect(url_for('user', userid=userid))
        elif request.method == 'GET':
            form.roleselect.data = user.role
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('select-role.html', user=user, form=form)

@app.route('/edit/section/<userid>', methods=['GET', 'POST'])
@login_required
def selectsection(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = selectSectionForm()
    if user.id == current_user.id or current_user.role=='admin':
        if form.validate_on_submit():
            user.section = form.sectionselect.data
            db.session.commit()
            return redirect(url_for('nameselection', userid=userid))
        elif request.method == 'GET':
            form.sectionselect.data = user.section
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('select-section.html', user=user, form=form)

@app.route('/edit/name/<userid>', methods=['GET', 'POST'])
@login_required
def nameselection(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    currentsection = user.section
    form = selectNameForm(currentsection)
    if user.id == current_user.id or current_user.role=='admin':
        if form.validate_on_submit():
            user.name = form.nameselect.data
            guest = Guest.query.filter_by(name=user.name).first_or_404()
            guest.email = user.email
            guest.registered = 'yes'
            db.session.commit()
            return redirect(url_for('currentlocation', userid=userid))
        elif request.method == 'GET':
            form.nameselect.data = user.name
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('select-user.html', user=user, form=form)

@app.route('/edit/location/<userid>', methods=['GET', 'POST'])
@login_required
def currentlocation(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = selectLocationForm()
    if user.id == current_user.id or current_user.role=='admin':
        if form.validate_on_submit():
            user.currentlocation = form.location.data
            db.session.commit()
            return redirect(url_for('user', userid=userid))
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('select-location.html', user=user, form=form)

@app.route('/edit/other/<userid>', methods=['GET', 'POST'])
@login_required
def nameother(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = nameOther()
    if user.id == current_user.id or current_user.role=='admin':
        if form.validate_on_submit():
            user.name = form.name.data
            db.session.commit()
            return redirect(url_for('currentlocation', userid=userid))
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user))
    return render_template('name-other.html', user=user, form=form)

@app.route('/edit/social/<userid>', methods=['GET', 'POST'])
@login_required
def socialLinks(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = editSocialLinksForm()
    if user.id == current_user.id or current_user.role=='admin':
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
            form.facebook.data = user.facebook
            form.twitter.data = user.twitter
            form.instagram.data = user.instagram
            form.linkedin.data = user.linkedin
            form.snapchat.data = user.snapchat
            form.reddit.data = user.reddit
            form.mastodon.data = user.mastodon
            form.tiktok.data = user.tiktok
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))
    return render_template('edit-social.html', user=user, form=form)

@app.route('/edit/reset/<userid>', methods=['GET','POST'])
@login_required
def resetProfile(userid):
    usertoreset = User.query.filter_by(id=userid).first_or_404()
    guestToReset= Guest.query.filter_by(email=usertoreset.email).first()
    email=usertoreset.email
    form = EmptyForm()
    if usertoreset.id == current_user.id or current_user.role=='admin':
        if usertoreset:
            usertoreset.name = ''
            usertoreset.section = ''
            usertoreset.rsvp = 'Not yet'
            if usertoreset.role == 'admin':
                usertoreset.role = 'admin'   
            else:
                usertoreset.role = ''   
            if guestToReset: 
                guestToReset.email = None
                guestToReset.registered = 'no'
                guestToReset.rsvp = 'Not yet'
            usertoreset.currentlocation = ''
            usertoreset.facebook = ''
            usertoreset.twitter = ''
            usertoreset.instagram = ''
            usertoreset.linkedin = ''
            usertoreset.snapchat = ''
            usertoreset.reddit = ''
            usertoreset.mastodon = ''
            usertoreset.tiktok = ''
        if guestToReset:
            guestToReset.email = None
            guestToReset.registered = 'no'
            guestToReset.rsvp = 'Not yet'
        db.session.commit()
        profile_reset_email(email=usertoreset.email, userid=usertoreset.id)
        flash("Your profile was reset.")
        return redirect(url_for('user', userid=userid))
        if current_user.id == 'admin':
            return redirect(url_for('adminusermanagement'))
        else:
            return redirect(url_for('user', userid=userid))
    else:
        flash("You can't edit someone else's profile!")
        return redirect(url_for('user', userid=current_user.id))


# Validation of uploaded photo
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format)

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/upload/<userid>', methods=['GET', 'POST'])
def upload_files(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    form = ProfilePictureForm()
    basedir = os.path.abspath(os.path.dirname(__file__))
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = uploaded_file.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                return "Invalid image", 400
            uploaded_file.save(os.path.join(basedir, app.config['UPLOAD_PATH'], 
                userid+file_ext))
            user.avatar = userid+file_ext
            db.session.commit()
        return redirect(url_for('user', userid=userid))
    return render_template('profile-picture.html', userid=userid, form = form)


@app.route('/rsvp/<userid>', methods=['GET', 'POST'])
@login_required
def rsvp(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    guest = Guest.query.filter_by(email=user.email).first()
    form = rsvpForm()

    if user.id == current_user.id or current_user.role=='admin':
        if user.name is None:
            flash("We need a bit more info fro you first.")
            return redirect(url_for('selectrole', userid=userid))    
        elif guest is None:
            if form.validate_on_submit():
                if form.rsvp.data == 'Yes, I plan to be there' or form.rsvp.data=='Yes, I will be there':
                    user.rsvp = 'yes'
                    db.session.commit()
                    new_rsvp_email(user=user)
                    flash("Thank you for RSVP'ing")
                    return redirect(url_for('user', userid=userid))
                else: 
                    user.rsvp = 'no'
                    db.session.commit()
                    new_rsvp_email(user=user)
                    flash("Thank you for RSVP'ing")
                    return redirect(url_for('user', userid=userid))
                return redirect(url_for('user', userid=userid))
            return render_template('rsvp.html', user=user, form=form)
        else: 
            if form.validate_on_submit():
                if form.rsvp.data == 'Yes, I plan to be there' or form.rsvp.data=='Yes, I will be there':
                    user.rsvp = 'yes'
                    guest.rsvp = 'yes'
                    db.session.commit()
                    new_rsvp_email(user=user)
                    flash("Thank you for RSVP'ing")
                    return redirect(url_for('user', userid=userid))
                else: 
                    user.rsvp = 'no'
                    guest.rsvp = 'no'
                    db.session.commit()
                    new_rsvp_email(user=user)
                    flash("Thank you for RSVP'ing")
                    return redirect(url_for('user', userid=userid))
                return redirect(url_for('user', userid=userid))
            return render_template('rsvp.html', user=user, form=form)
    else:
        flash("You can't edit someone else's rsvp!")
        return redirect(url_for('user', userid=current_user.id))

    return render_template('rsvp.html', userid=userid, form = form)

#
# PUBLIC -----------------------------------------------------------------------
# 

@app.route('/public/<guestid>', methods=['GET'])
@login_required
def public(guestid):
    guest = Guest.query.filter_by(id=guestid).first()
    user = User.query.filter_by(email=guest.email).first()
    if guest.email is None:
        flash("This person has not registered yet.")
        return redirect(url_for('user', userid=current_user.id))
    else:
        return render_template('public.html', guestid=guestid, user=user)
    return render_template('public.html', guestid=guestid, user=user)

@app.route('/public/other/<userid>', methods=['GET'])
@login_required
def publicother(userid):
    user = User.query.filter_by(id=userid).first()
    if user.role !='I graduated in 2005':
        return render_template('public-other.html', userid=userid, user=user)


@app.route('/reconnect', methods=['GET', 'POST'])
@login_required
def reconnect():
    guests = Guest.query.order_by(Guest.section.asc())
    friends = User.query.filter_by(role='I was friends with people who graduated in 2005').order_by(User.name.asc())
    teachers = User.query.filter_by(role='I was a teacher at the EEB2').order_by(User.name.asc())
    others = User.query.filter_by(role='Other').order_by(User.name.asc())
    form = inviteForm()
    return render_template('reconnect.html', guests=guests, friends=friends, 
        teachers=teachers, others=others)

@app.route('/invite/<guestid>', methods=['GET', 'POST'])
@login_required
def invite(guestid):
    guest = Guest.query.filter_by(id=guestid).first()
    form = inviteForm()
    if form.validate_on_submit():
        email = form.email.data
        captcha = form.captcha.data
        if captcha == '3' or captcha == 'three' or captcha == 'Three':
            send_invite_email(email=email, captcha=captcha)
            flash("Thank you, the invite has been sent.")
            return redirect(url_for('reconnect', userid=current_user.id))
        else: 
            flash("Check the captcha real quick?")
            return render_template('invite.html', guest=guest, form=form)
    return render_template('invite.html', guest=guest, form=form)


@app.route('/memory-lane', methods=['GET'])
@login_required
def memory_lane():
    return render_template('memory-lane.html')


#
# ADMIN ------------------------------------------------------------------------
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

@app.route('/admin/rsvp', methods=['GET'])
@login_required
def adminrsvpmanagement():
    if current_user.role == 'admin':
        users = User.query.filter(User.rsvp.in_(('yes', 'no'))).order_by(User.id.asc())
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))
    return render_template("rsvp_management.html", title='User management', 
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

@app.route('/admin/toggleverify/<userid>', methods=['GET', 'POST'])
@login_required
def toggleverify(userid):
    if current_user.role == 'admin':
        user = User.query.filter_by(id=userid).first()
        form = EmptyForm()
        user.verified = 'yes'
        db.session.commit()
        flash('Your changes have been saved: the user email is verified.')
        return redirect(url_for('adminusermanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))
    return redirect(url_for('adminusermanagement'))

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
                guestToClear.rsvp = 'Not yet'
            db.session.delete(usertodelete)
            db.session.commit()
            flash('User was deleted.')
            return redirect(url_for('adminusermanagement'))
        return redirect(url_for('adminusermanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))

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
        friends = User.query.filter_by(role='I was friends with people who graduated in 2005').order_by(User.name.asc())
        teachers = User.query.filter_by(role='I was a teacher at the EEB2').order_by(User.name.asc())
        others = User.query.filter_by(role='Other').order_by(User.name.asc())

        form = AddGuestForm()
        if form.validate_on_submit():
            g = Guest(name=form.guestname.data.title(), section=form.section.data.upper(), 
                registered="no", rsvp="Not yet")
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
    return render_template("guest_management.html", title='Guest list management', 
        guests=guests, friends=friends, teachers=teachers, others=others, form=form)

@app.route('/edit/reset/guest/<guestid>', methods=['GET','POST'])
@login_required
def resetGuest(guestid):
    form = EmptyForm()
    guesttoreset = Guest.query.filter_by(id=guestid).first()
    usertoreset = User.query.filter_by(email = guesttoreset.email).first()
    if current_user.role == 'admin':
        if guesttoreset:
            guesttoreset.email = None
            guesttoreset.registered = 'no'
            guesttoreset.rsvp = 'Not yet'
        if usertoreset: 
            usertoreset.name = ''
            usertoreset.section = ''
            usertoreset.currentlocation = ''
            if usertoreset.role == 'admin':
                usertoreset.role = 'admin'   
            else:
                usertoreset.role = ''  
            usertoreset.rsvp = 'Not yet'
        db.session.commit()
        return redirect(url_for('adminguestmanagement'))
    else:
        flash("Only admins can reset guest profiles.")
        return redirect(url_for('user', userid=current_user.id))

@app.route('/admin/delete/guest/<guestid>', methods=['GET', 'POST'])
@login_required
def delete_guest(guestid):
    currentguest = Guest.query.filter_by(id=guestid).first()
    user = User.query.filter_by(email=currentguest.email).first()
    if current_user.role == 'admin':
        if user:
            user.name = ''
            user.section = ''
        db.session.delete(currentguest)
        db.session.commit()
        flash('Guest was deleted.')
        return redirect(url_for('adminguestmanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))