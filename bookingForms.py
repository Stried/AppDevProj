from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from datetime import date, datetime

import shelve

def all_numbers(form,field):
    if field.data.isdigit()==False:
        raise ValidationError("Field must be all numbers")

def is_future(form,field):
    if field.data<=date.today():
        raise ValidationError("Cannot select date")

facilDict = {}
facilDB = shelve.open('Facilities')
try:    
    if 'Facilities' in facilDB:
        facilDict = facilDB['Facilities']
    else:
        facilDB['Facilities'] = facilDict
except:
    print('Error in retrieving Facilities.')

facilityIDList = []
facilityUIDList = []
facilityLocationList = []

for facil in facilDict:
    facils = facilDict.get(facil)
    facilAvailability = facils.get_fac_status()
    if facilAvailability == 'Available':
        facilityUID = facils.get_uniqueID()
        facilityUIDList.append(facilityUID)
        
        facilityID = facils.get_fac_id()
        facilityIDList.append(facilityID)
        
        facilityLocation = facils.get_fac_loc()
        facilityLocationList.append(facilityLocation)

bookingFacilDict = {}
bookingFacilDB = shelve.open('BookingFacil')
try:
    if 'BookingFacil' in bookingFacilDB:
        bookingFacilDict = bookingFacilDB['BookingFacil']
    else:
        bookingFacilDB['BookingFacil'] = bookingFacilDict
except:
    print('Error in retrieving bookings.')

class bookingForm(FlaskForm):
    bookingFacilityID = SelectField('Facility: ',  
                                 validators=[DataRequired()])
    bookingDate = DateField('Booking Date: ',
                                validators=[InputRequired(), is_future],
                                default=date.today(),
                                render_kw={'placeholder' : 'DD-MM-YY'})
    bookingTimeSlot = SelectField('Booking Timeslot: ',
                                    validators=[DataRequired()],
                                    choices=[('', 'Select Timeslot'), ('10am to 11am', '10am to 11am'), ('11am to 12pm', '11am to 12pm'), ('12pm to 1pm', '12pm to 1pm'), ('1pm to 2pm', '1pm to 2pm'), ('2pm to 3pm', '2pm to 3pm'), ('3pm to 4pm', '3pm to 4pm'), ('4pm to 5pm', '4pm to 5pm'), ('5pm to 6pm', '5pm to 6pm'), ('6pm to 7pm', '6pm to 7pm')])
    submit = SubmitField('Continue')

class paymentForm(FlaskForm):
    paymentMethod = SelectField('Payment Method: ',
                                validators=[DataRequired()],
                                choices=[('', 'Select Payment Method'), ('American Express', 'American Express'), ('Mastercard', 'Mastercard'), ('VISA', 'VISA')])
    cardNumber = StringField('Card Number: ',
                            validators=[DataRequired(), all_numbers, Length(min = 12, max = 12)],
                            render_kw={'placeholder' : 'Input Card Number'})
    expirationDate = DateField('Expiration Date: ',
                                validators=[DataRequired(), is_future],
                                default=date.today())
    securityPIN = StringField('Security PIN: ',
                               validators=[DataRequired(), all_numbers, Length(min = 3, max = 3)],
                               render_kw={'placeholder' : 'Input Security PIN'})
    submit = SubmitField('Book Facility')
    
class bookingSortForm(FlaskForm):
    selectData = SelectField('Facility: ',  
                                 validators=[DataRequired()])
    submit = SubmitField('Sort')
# Set restrictions using data from facilitiesdb