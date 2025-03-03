from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, BooleanField, TimeField, DateField, SubmitField
from wtforms.validators import DataRequired, Length , number_range ,Regexp , ValidationError
from datetime import date

# custom validators:--------------------------------------------

def numav_required(form, field):
    if form.NAVIG.data and not field.data:
        raise ValidationError('Aircraft Number is required if Navigator is true.')

def conditional_number_range(form, field):
    if form.NAVIG.data:
        if field.data is None or field.data < 1:
            raise ValidationError('Aircraft Number must be  a valide number and at least 1.')

#  flask forms:------------------------------------------------

class deleteAircraftForm(FlaskForm):
    id = IntegerField('Aircraft Number', validators=[DataRequired(), number_range(min=1)])
    submit = SubmitField('Delete')

class deleteFlightForm(FlaskForm):
    id = IntegerField('flight Number', validators=[DataRequired(), number_range(min=1)])
    submit = SubmitField('Delete')
class deleteEmployeForm(FlaskForm):
    id = IntegerField('Employe Number', validators=[DataRequired(), number_range(min=1)])
    submit = SubmitField('Delete')

class VolForm(FlaskForm):
    NUMVOL = IntegerField('Flight Number')
    VILDEP = StringField('Departure City', validators=[DataRequired(), Length(max=50)])
    VILARR = StringField('Arrival City', validators=[DataRequired(), Length(max=50)])
    # HDEP = DateTimeField('Departure Time', format='%Y-%m-%dT%H:%M:%S', validators=[DataRequired()])
    DURVOL = IntegerField('flight Duration', validators=[DataRequired()])
    NUMAV = IntegerField('Aircraft Number', validators=[number_range(min=1)])
    submit = SubmitField('Submit')

class AvionForm(FlaskForm):
    NUMAV = IntegerField('Aircraft Number')
    TYPAV = StringField('Aircraft Type', validators=[DataRequired(), Length(max=10)])
    DATMS = DateField('Service Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    DATREV = DateField('inspection Start Date', format='%Y-%m-%d')
    NBHDDREV = IntegerField('Hours From Last Inspection',)
    AUTORISTION = BooleanField('Authorization')
    submit = SubmitField('Submit')

class RevisionForm(FlaskForm):
    NUMREV = IntegerField('Inspection Number')
    ANOMA = StringField('Anomaly', validators=[DataRequired(), Length(max=1000)])
    REP_EFF = StringField('Repairs done', validators=[DataRequired(), Length(max=1000)])
    ORG_CHANG = StringField('Changed Part', validators=[DataRequired(), Length(max=1000)])
    AVIS = BooleanField('Verdict', default=False)
    NUMAV = IntegerField('Aircraft Number', validators=[DataRequired(), number_range(min=1)])
    submit = SubmitField('Submit')

class JourDeVolForm(FlaskForm):
    JVOL = StringField('Flight Day', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

class EstPlanifieForm(FlaskForm):
    NUMVOL = IntegerField('Flight Number', validators=[DataRequired()])
    JVOL = StringField('Flight Day', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

class EscaleForm(FlaskForm):
    NOORD = IntegerField('Order Number', validators=[DataRequired()])
    VILESC = StringField('Stopover City', validators=[DataRequired(), Length(max=50)])
    HARRESC = DateTimeField('Stopover Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    DUREESC = TimeField('Stopover Duration', format='%H:%M:%S', validators=[DataRequired()])
    NUMVOL = IntegerField('Flight Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PersonneForm(FlaskForm):
    NUMEMP = IntegerField('Employee Number')
    NOM = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    PRENOM = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    TEL = StringField('Phone Number', validators=[DataRequired(), Length(max=15)])
    TEL = StringField('Phone Number', validators=[DataRequired(), Length(max=15), 
                                        Regexp(r'^\+?\d+[-\s]?\d+$', message="Invalid phone number. you can use one 'space' or one '-' after the country code")])
    ADRESSE = StringField('Address', validators=[DataRequired(), Length(max=100)])
    VILLE = StringField('City', validators=[DataRequired(), Length(max=50)])
    CODE_POST = StringField('Postal Code', validators=[DataRequired(), Length(max=20)])
    PAYS = StringField('Country', validators=[DataRequired(), Length(max=255)])
    SAL = IntegerField('Salary', validators=[DataRequired(), number_range(min=0)])
    FONCTION = StringField('Function / Job', validators=[DataRequired(), Length(max=50)])
    DATEMB = DateField('Hire Date', format='%Y-%m-%d', default=date.today)
    NBMHV = IntegerField('Monthly Flight Hours',default=0, validators=[number_range(min=0)])
    NBTHV = IntegerField('Total Flight Hours', validators=[number_range(min=0)])
    NAVIG = BooleanField('Navigator', default=False)
    NUMAV = IntegerField('Aircraft Number',default=0, validators=[numav_required, conditional_number_range])
    submit = SubmitField('Submit')

class PersonneUpdateForm(FlaskForm):
    NUMEMP = IntegerField('Employee Number',validators=[DataRequired(), number_range(min=1)])
    NOM = StringField('Last Name', validators=[Length(max=50)])
    PRENOM = StringField('First Name', validators=[Length(max=50)])
    TEL = StringField('Phone Number', validators=[Length(max=15)])
    TEL = StringField('Phone Number', validators=[Length(max=15), 
                                        Regexp(r'^\+?\d+[-\s]?\d+$', message="Invalid phone number. you can use one 'space' or one '-' after the country code")])
    ADRESSE = StringField('Address', validators=[Length(max=100)])
    VILLE = StringField('City', validators=[Length(max=50)])
    CODE_POST = StringField('Postal Code', validators=[Length(max=20)])
    PAYS = StringField('Country', validators=[Length(max=255)])
    SAL = IntegerField('Salary', validators=[number_range(min=0)])
    FONCTION = StringField('Function / Job', validators=[Length(max=50)])
    # DATEMB = DateField('Hire Date', format='%Y-%m-%d', default=date.today)
    NBMHV = IntegerField('Monthly Flight Hours',default=0, validators=[number_range(min=0)])
    # NBTHV = IntegerField('Total Flight Hours', validators=[number_range(min=0)])
    NAVIG = BooleanField('Navigator', default=False)
    NUMAV = IntegerField('Aircraft Number',default=0, validators=[numav_required, conditional_number_range])
    submit = SubmitField('Submit')


# o value for personne.numav mean no arircraft  is connected to this person changed to null in main.py