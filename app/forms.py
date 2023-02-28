from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Guest, Section


class LoginForm(FlaskForm):
    username = StringField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AddSectionForm(FlaskForm):
    sectioninput = StringField('', validators=[DataRequired()])
    submit = SubmitField('Add section')

    def validate_sectioninput(self, sectioninput):
        sq = Section.query.filter_by(section=sectioninput.data.upper()).first()
        if sq is not None:
            raise ValidationError('This section already exists.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

def fetch_section():      
    return db.session.query(Section).all()

class AddGuestForm(FlaskForm):
    guestname = StringField('Name', validators=[DataRequired()])
    section = SelectField(u'Section', choices = [], validators = [DataRequired()])
    submit = SubmitField('Add guest')

    def __init__(self):
        super(AddGuestForm, self).__init__()
        self.section.choices = Section.query.order_by(Section.section.asc()).all()

class selectRoleForm(FlaskForm):
    roleselect = SelectField(u'', choices = [(''),('I graduated in 2005'),
        ('I was friends with people who graduated in 2005'),('I was a teacher at the EEB2'),
        ('Other')], validators = [DataRequired()])
    submit = SubmitField('Next')


class selectSectionForm(FlaskForm):
    sectionselect = SelectField(u'Section', choices = [], validators = [DataRequired()])
    submit = SubmitField('Next')

    def __init__(self):
        super(selectSectionForm, self).__init__()
        self.sectionselect.choices = Section.query.order_by(Section.section.asc()).all()

class selectNameForm(FlaskForm):
    nameselect = SelectField(u'Name', choices = [], validators = [DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, currentsection):
        super(selectNameForm, self).__init__()
        self.nameselect.choices = Guest.query.filter_by(email=None).filter_by(section=currentsection).order_by(Guest.name.asc()).all()

class editSocialLinksForm(FlaskForm):
    facebook = StringField('Facebook', validators=[])
    twitter = StringField('Twitter', validators=[])
    instagram = StringField('Instagram', validators=[])
    linkedin = StringField('LinkedIn', validators=[])
    snapchat = StringField('Snapchat', validators=[])
    reddit = StringField('Reddit', validators=[])
    mastodon = StringField('Mastodon', validators=[])
    tiktok = StringField('TikTok', validators=[])
    submit = SubmitField('Save')

class nameOther(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data.title()).first()
        guest = Guest.query.filter_by(name=name.data.title()).first()
        if user is not None:
            raise ValidationError('Please use a different name.')
        if guest is not None:
            raise ValidationError('Please use a different name.')

class ProfilePictureForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')
