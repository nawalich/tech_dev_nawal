from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Time, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker ,declarative_base , relationship

from flask import Flask , render_template , url_for , redirect, flash , request
from forms import VolForm, AvionForm, RevisionForm, JourDeVolForm, EstPlanifieForm, EscaleForm, PersonneForm , deleteAircraftForm , deleteEmployeForm ,PersonneUpdateForm ,deleteFlightForm

from datetime import date, datetime


# user - database credentials
username = 'root'

password = 'root'
host = 'localhost'
port = '3306'  # Default MySQL port
database = 'airline_db'
# Create the connection string
connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
# Create the engine
engine = create_engine(connection_string)
# create base class
Base = declarative_base()
# create classes
class Vol(Base):
    __tablename__ = 'VOL'
    NUMVOL = Column(Integer, primary_key=True)
    VILDEP = Column(String(50))
    VILARR = Column(String(50))
    HDEP = Column(DateTime)
    DURVOL = Column(Integer)
    NUMAV = Column(Integer, ForeignKey('AVION.NUMAV'))
    
    avion = relationship("Avion", back_populates="vols")
    escales = relationship("Escale", back_populates="vol")
    planifications = relationship("EstPlanifie", back_populates="vol")

class Avion(Base):
    __tablename__ = 'AVION'
    NUMAV = Column(Integer, primary_key=True)
    TYPAV = Column(String(10))
    DATMS = Column(Date)
    DATREV = Column(Date)
    NBHDDREV = Column(Integer)
    AUTORISTION = Column(Boolean)

    vols = relationship("Vol", back_populates="avion")
    revisions = relationship("Revision", back_populates="avion")
    personnel = relationship("Personne", back_populates="avion")

class Revision(Base):
    __tablename__ = 'REVISION'
    NUMREV = Column(Integer, primary_key=True)
    ANOMA = Column(String(1000))
    REP_EFF = Column(String(1000))
    ORG_CHANG = Column(String(1000))
    AVIS = Column(Boolean)
    DATREV = Column(Date)
    NBHREV = Column(Integer)
    NUMAV = Column(Integer, ForeignKey('AVION.NUMAV'))

    avion = relationship("Avion", back_populates="revisions")

class JourDeVol(Base):
    __tablename__ = 'JOUR_DE_VOL'
    JVOL = Column(String(20), primary_key=True)

    planifications = relationship("EstPlanifie", back_populates="jour")

class EstPlanifie(Base):
    __tablename__ = 'EST_PLANIFIE'
    NUMVOL = Column(Integer, ForeignKey('VOL.NUMVOL'), primary_key=True)
    JVOL = Column(String(20), ForeignKey('JOUR_DE_VOL.JVOL'), primary_key=True)

    vol = relationship("Vol", back_populates="planifications")
    jour = relationship("JourDeVol", back_populates="planifications")

class Escale(Base):
    __tablename__ = 'ESCALE'
    NOORD = Column(Integer, primary_key=True)
    VILESC = Column(String(50))
    HARRESC = Column(DateTime)
    DUREESC = Column(Time)
    NUMVOL = Column(Integer, ForeignKey('VOL.NUMVOL'))

    vol = relationship("Vol", back_populates="escales")

class Personne(Base):
    __tablename__ = 'PERSONNE'
    NUMEMP = Column(Integer, primary_key=True)
    NOM = Column(String(50))
    PRENOM = Column(String(50))
    TEL = Column(String(15))
    ADRESSE = Column(String(100))
    VILLE = Column(String(50))
    CODE_POST = Column(String(20))
    PAYS = Column(String(255))
    SAL = Column(Integer)
    FONCTION = Column(String(50))
    DATEMB = Column(Date)
    NBMHV = Column(Integer)
    NBTHV = Column(Integer)
    NAVIG = Column(Boolean)
    NUMAV = Column(Integer, ForeignKey('AVION.NUMAV'))

    avion = relationship("Avion", back_populates="personnel")
# create tables in database
# ! Comment the line below after the first run 
#  ! uncomment for the first run
# Base.metadata.create_all(engine)
# create session
Session = sessionmaker(bind=engine) # Link the session to the engine
session = Session()


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# dashboard:-----------------------------------------------------------------------------
@app.route("/")
@app.route("/index")
def home():
    # Query all data from the tables
    datetimeNow= datetime.now()
    dateNow = datetime.now().date()
    aircrafts = session.query(Avion).all()
    employees = session.query(Personne).all()
    flights = session.query(Vol).all()
    return render_template('index.html',title="Dashboard",menu="Home",aircrafts=aircrafts,employees=employees,flights=flights,datetimeNow=datetimeNow,dateNow=dateNow)

# aircrafts routes:-------------------------------------------------------------------------
@app.route("/update-delete-aircrafts.html", methods=['GET', 'POST'])
def air_update_delete():
    form = deleteAircraftForm()
    if form.validate_on_submit():
        ID = form.id.data
        try:
            # Query the aircraft by ID and delete it
            aircraft = session.query(Avion).filter_by(NUMAV=ID).first()
            if aircraft:
                session.delete(aircraft)
                session.commit()
                flash(f'Aircraft with ID = {ID} deleted permanently!', 'danger')
            else:
                flash(f'Aircraft with ID = {ID} not found.', 'warning')
        except Exception as e:
            session.rollback()
            flash(f'Error deleting aircraft: {str(e)}', 'danger')
        return redirect(url_for('air_update_delete'))
    return render_template('update-delete-aircrafts.html',title="update-delete-aircrafts",menu="Aircrafts",form=form)

@app.route("/forms-aircrafts.html", methods=['GET', 'POST'])
def air_forms():
    form = AvionForm()
    if form.validate_on_submit():
        try:
            new_aircraft = Avion(
                TYPAV=form.TYPAV.data,
                DATMS=form.DATMS.data,
                DATREV=form.DATMS.data,
                NBHDDREV=0,
                AUTORISTION=True
            )
            session.add(new_aircraft)
            session.commit()
            flash('Aircraft added successfully!', 'success')
            return redirect(url_for('air_forms'))
        except Exception as e:
            session.rollback()
            flash(f'Error adding aircraft: {str(e)}', 'danger')
            return redirect(url_for('air_forms'))
    return render_template('forms-aircrafts.html', title="insert-aircrafts", menu="Aircrafts", form=form)


# flights routes:-------------------------------------------------------------------------
@app.route("/insert-flight.html", methods=['GET', 'POST'])
def flight_insert():
    form = VolForm()
    if request.method == 'POST':
        departure_time = request.form['HDEP']
        if form.validate_on_submit():
            if form.NUMAV.data:
                # Check if the aircraft exists
                aircraft = session.query(Avion).filter_by(NUMAV=form.NUMAV.data).first()
                if not aircraft:
                    flash(f'Aircraft with ID {form.NUMAV.data} does not exist.', 'danger')
                    return redirect(url_for('flight_insert'))
                # Check if the aircraft is authorized
                if aircraft and aircraft.AUTORISTION == False:
                    flash(f'Aircraft with ID {form.NUMAV.data} IS << not authorized >>.', 'danger')
                    return redirect(url_for('flight_insert'))
                # Verify if the aircraft is already in a flight
                existing_flight = session.query(Vol).filter_by(NUMAV=form.NUMAV.data).all()
                if existing_flight:
                    for flight in existing_flight:
                        if flight.HDEP == departure_time:
                            flash(f'Aircraft with ID {form.NUMAV.data} is already assigned to flight with ID ({flight.NUMVOL}) at that DATE and TIME.', 'warning')
                            return redirect(url_for('flight_insert'))
            try:
                new_vol = Vol(
                    NUMVOL=form.NUMVOL.data,
                    VILDEP=form.VILDEP.data,
                    VILARR=form.VILARR.data,
                    HDEP=departure_time,
                    DURVOL=form.DURVOL.data,
                    NUMAV=form.NUMAV.data)
                # Commit the changes
                session.add(new_vol)
                session.commit()
                # Update the aircraft's flight hours
                aircraft = session.query(Avion).filter_by(NUMAV=form.NUMAV.data).first()
                if aircraft:
                    aircraft.NBHDDREV += form.DURVOL.data
                    session.commit()
                flash('Flight added successfully!', 'success')
                return redirect(url_for('flight_insert'))
            except Exception as e:
                session.rollback()
                flash(f'Error adding flight: {str(e)}', 'danger')
                return redirect(url_for('flight_insert'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{form[field].label.text}: {error}', 'warning')
    return render_template('insert-flight.html', title="Insert Flight", menu="Flights", form=form)


@app.route("/update-delete-flight.html", methods=['GET', 'POST'])
def flight_update_delete():
    form_delete = deleteFlightForm()
    if form_delete.validate_on_submit():
        ID = form_delete.id.data
        try:
            # Query the flight by ID and delete it
            flight = session.query(Vol).filter_by(NUMVOL=ID).first()
            if flight:
                session.delete(flight)
                session.commit()
                flash(f'Flight with ID = {ID} deleted permanently!', 'danger')
            else:
                flash(f'Flight with ID = {ID} not found.', 'warning')
        except Exception as e:
            session.rollback()
            flash(f'Error deleting flight: {str(e)}', 'danger')
        return redirect(url_for('flight_update_delete'))
    return render_template('update-delete-flight.html',title="update-delete-flight",menu="Flights",form_delete=form_delete)


# employees routes:-------------------------------------------------------------------------
@app.route("/insert-employe.html", methods=['GET', 'POST'])
def employe_insert():
    form = PersonneForm()
    if form.validate_on_submit():
        if form.NUMAV.data:
            # Check if the aircraft exists
            aircraft = session.query(Avion).filter_by(NUMAV=form.NUMAV.data).first()
            if not aircraft:
                flash(f'Aircraft with ID {form.NUMAV.data} does not exist.', 'danger')
                return redirect(url_for('employe_insert'))
        try:
            new_Employe = Personne(
                NOM = form.NOM.data,
                PRENOM = form.PRENOM.data,
                TEL = form.TEL.data,
                ADRESSE = form.ADRESSE.data,
                VILLE = form.VILLE.data,
                CODE_POST = form.CODE_POST.data,
                PAYS = form.PAYS.data,
                SAL = form.SAL.data,
                FONCTION = form.FONCTION.data,
                DATEMB = form.DATEMB.data,  # default=date.today so i dind't use form.DATEMB on html form
                NBMHV = 0,
                NBTHV = form.NBTHV.data,
                NAVIG = form.NAVIG.data,
                NUMAV = form.NUMAV.data if form.NAVIG.data else None,
            )
            session.add(new_Employe)
            session.commit()
            flash('Employe added successfully!', 'success')
            return redirect(url_for('employe_insert'))
        except Exception as e:
            session.rollback()
            flash(f'Error adding Employe: {str(e)}', 'danger')
            return redirect(url_for('employe_insert'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'warning')
    return render_template('insert-employe.html',title="insert-employe",menu="Employees",form=form)   

@app.route("/employe-update-delete.html", methods=['GET', 'POST'])
def employe_update_delete():
    form_delete = deleteEmployeForm()
    form = PersonneUpdateForm()

    # Handle delete form submission
    if form_delete.validate_on_submit():
        ID = form_delete.id.data
        try:
            # Query the employee by ID and delete it
            employe = session.query(Personne).filter_by(NUMEMP=ID).first()
            if employe:
                session.delete(employe)
                session.commit()
                flash(f'Employee with ID = {ID} deleted permanently!', 'danger')
            else:
                flash(f'Employee with ID = {ID} not found.', 'warning')
        except Exception as e:
            session.rollback()
            flash(f'Error deleting employee: {str(e)}', 'danger')
        return redirect(url_for('employe_update_delete'))

    # Handle update form submission 
    elif form.validate_on_submit():
        if form.NUMEMP.data:
            # Check if the employee exists
            employee = session.query(Personne).filter_by(NUMEMP=form.NUMEMP.data).first()
            if not employee:
                flash(f'Employee with ID {form.NUMEMP.data} does not exist.', 'warning')
                return redirect(url_for('employe_update_delete'))
        try:
            # Get the existing employee
            employee = session.query(Personne).filter_by(NUMEMP=form.NUMEMP.data).first()
            # Update fields
            employee.NOM = form.NOM.data
            employee.PRENOM = form.PRENOM.data
            employee.TEL = form.TEL.data
            employee.ADRESSE = form.ADRESSE.data
            employee.VILLE = form.VILLE.data
            employee.CODE_POST = form.CODE_POST.data
            employee.PAYS = form.PAYS.data
            employee.SAL = form.SAL.data
            employee.FONCTION = form.FONCTION.data
            employee.NBMHV = form.NBMHV.data
            employee.NBTHV = employee.NBTHV # we keep the total flight hours unchanged
            employee.NAVIG = form.NAVIG.data
            employee.NUMAV = form.NUMAV.data if form.NAVIG.data else None
            # Commit the changes
            session.commit()
            flash('Employee updated successfully!', 'success')
        except Exception as e:
            session.rollback()
            flash(f'Error updating Employee: {str(e)}', 'danger')
        return redirect(url_for('employe_update_delete'))

    # Handle form validation errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field}: {error}', 'warning')
    return render_template('employe-update-delete.html',title="update-delete-employe",menu="Employees",form=form,form_delete=form_delete)


# inspection routes:-------------------------------------------------------------------------
@app.route("/inspection.html", methods=['GET', 'POST'])
def inspection_insert():
    form = RevisionForm()
    if form.validate_on_submit():
        if form.NUMAV.data:
            # Check if the aircraft exists
            aircraft = session.query(Avion).filter_by(NUMAV=form.NUMAV.data).first()
            if not aircraft:
                flash(f'Aircraft with ID {form.NUMAV.data} does not exist.', 'warning')
                return redirect(url_for('inspection_insert'))
        try:
            # SLECT the aircraft to update it and get nbhddrev t save as number of hours on inspection
            aircraft = session.query(Avion).filter_by(NUMAV=form.NUMAV.data).first()
            # add new inspection
            new_Revision = Revision(
                ANOMA = form.ANOMA.data,
                REP_EFF = form.REP_EFF.data,
                ORG_CHANG = form.ORG_CHANG.data,
                AVIS = form.AVIS.data if form.AVIS.data else False,
                NUMAV = form.NUMAV.data,
                DATREV = date.today(),
                NBHREV = aircraft.NBHDDREV
            )
            session.add(new_Revision)
            # updating the inspected aircraft 
            aircraft.DATREV = date.today()
            aircraft.NBHDDREV = 0
            aircraft.AUTORISTION = form.AVIS.data
            # Commit the changes
            session.commit()
            flash('Inspection added successfully!', 'success')
            flash('aircraft data updated successfully!', 'success')
            return redirect(url_for('inspection_insert'))
        except Exception as e:
            session.rollback()
            flash(f'Error adding Inspection: {str(e)}', 'danger')
            return redirect(url_for('inspection_insert'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'warning')
    
    return render_template('inspection.html',title="new-inspection",menu="Inspection",form=form)

@app.route("/inspection-check.html")
def inspection_check():
    # Query all revisions from the database
    revisions = session.query(Revision).all()
    return render_template('inspection-check.html', title="inspection-check", menu="Inspection", revisions=revisions)


# error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages-error-404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)