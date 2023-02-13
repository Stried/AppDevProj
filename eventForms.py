from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from datetime import datetime, date
import time
import shelve
        
class eventLocationCreateForm(FlaskForm):
    eventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'),
                                         ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    
    submit = SubmitField('Next ')

class eventCreateForm(FlaskForm):
    eventName = StringField('Event Name :', 
                            validators=[DataRequired(), Length(min = 2, max = 30)])
    eventDesc = TextAreaField('Event Description : ',
                            validators=[DataRequired(), Length(min = 2)])
    eventVacancy = IntegerField('Event Vacancy : ',
                                validators=[DataRequired()])
    
    eventDate = DateField('Event End Date : ',
                              validators=[DataRequired()],
                              format='%Y-%m-%d', #datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    eventDateTime = TimeField('Event End Time : ',
                              validators=[DataRequired()],
                              format='%H:%M',
                              render_kw={'placeholder' : 'HH:MM:SS'})
    
    eventStartDate = DateField('Event Start Date : ',
                              validators=[DataRequired()],
                              format='%Y-%m-%d', #datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    eventStartDateTime = TimeField('Event Start Time : ',
                                   validators=[DataRequired()],
                                   format='%H:%M',
                                   render_kw={'placeholder' : 'HH:MM:SS'})
    
    eventID = IntegerField('Event ID : ',
                           validators=[DataRequired(message="This field is required."), NumberRange(min=1000, max=9999)],
                           render_kw={'placeholder' : '001'})
    eventType = RadioField('Event Type : ',
                           validators=[DataRequired(message='An event type is required!')],
                           choices=[('Sports', 'Sports'), ('Lifestyle', 'Lifestyle'), ('Others', 'Others')])
    eventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    eventVenue = SelectField('Event Venue : ',
                             validators=[DataRequired()],
                             )
    eventStatus = SelectField('Event Status : ',
                              validators=[DataRequired()],
                              choices=[('', 'Select'), ('Active', 'Active'), ('Closed', 'Closed')])
    submit = SubmitField('Create Events')
    
    
    def validate_eventID(self, eventID):
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
        
        for keys in eventsDict:
            if self.eventID.data == eventsDict[keys].get_eventID():
                raise ValidationError('Event ID already taken!')
        
    def validate_eventVacancy(self, eventVenue):
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
            
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
        facilitySlotsList = []
        for facil in facilDict:
            facils = facilDict.get(facil)
            facilAvailability = facils.get_fac_status()
            if facilAvailability == 'Available':             
                facilityID = facils.get_fac_id()
                facilityIDList.append(facilityID)
                
                facilitySlots = facils.get_fac_slots()
                facilitySlotsList.append(facilitySlots)
                
        eventVenueChosen = self.eventVenue.data
        eventVacancyChosen = self.eventVacancy.data
        if eventVenueChosen in facilityIDList:
            index = facilityIDList.index(eventVenueChosen)
            if eventVacancyChosen > facilitySlotsList[index]:
                raise ValidationError(f'Max Event Vacancies is {facilitySlotsList[index]}!')
            
        print(facilityIDList)
        
    def validate_eventDate(self, eventDate): # Dont touch this.
        pre_dateCheck = "%Y-%m-%d"
        dateFormat = "%d%m%y"
        timeFormat = "%H%M%S"
        dateToday = date.today()
        
        startDate = ((self.eventStartDate.data).strftime(dateFormat) + (self.eventStartDateTime.data).strftime(timeFormat))
        print(f'Start Date : {startDate}')
        
        endDate = ((self.eventDate.data).strftime(dateFormat) + (self.eventDateTime.data).strftime(timeFormat))
        print(f'End Date : {endDate}')
        
        
        if int((self.eventDate.data).strftime(dateFormat)) < int(dateToday.strftime(dateFormat)): # 300222 < 310122
            raise ValidationError(f"End Date cannot be behind today. Today's Date {dateToday}")
        
        if int(endDate) < int(startDate): # 30122 < 31
            print('Please work man')
            raise ValidationError('End Date cannot be before Start Date')
        
    def validate_eventStartDate(self, eventStartDate):
        dateFormat = "%d%m%y"
        dateToday = date.today()
                
        if int((self.eventStartDate.data).strftime(dateFormat)) < int(dateToday.strftime(dateFormat)):
            raise ValidationError(f"End Date cannot be behind today. Today's Date {dateToday}")

class eventEditForm2(FlaskForm):
    editEventName = StringField('Edit Event Name : ',
                                validators=[],
                                render_kw={'placeholder' : 'Leave empty if no change.'})
    editEventDesc = TextAreaField('Edit Event Descriptrion : ',
                                  validators=[],
                                  render_kw={'placeholder' : 'Leave empty if no change.'})
    editEventVacancy = IntegerField('Edit Event Vacancy : ',
                               validators=[],
                               render_kw={'placeholder' : 'Leave empty if no change.'})
    
    editEventDate = DateField('Event End Date : ',
                              validators=[DataRequired()],
                              format='%Y-%m-%d',#datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    editEventDateTime = TimeField('Event End Time : ',
                              validators=[DataRequired()],
                              format='%H:%M',
                              render_kw={'placeholder' : 'HH:MM:SS'})
    
    editEventStartDate = DateField('Event Start Date : ',
                              validators=[DataRequired()],
                              format='%Y-%m-%d',
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    editEventStartDateTime = TimeField('Event Start Time : ',
                                   validators=[DataRequired()],
                                   format='%H:%M',
                                   render_kw={'placeholder' : 'HH:MM:SS'})
    
    editEventType = RadioField('Edit Event Type : ',
                               validators=[DataRequired()],
                               choices=[('Sports', 'Sports'), ('Lifestyle', 'Lifestyle'), ('Others', 'Others')])
    editEventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    editEventVenue = SelectField('Event Venue : ',
                             validators=[DataRequired()])
    editEventStatus = SelectField('Event Status : ',
                              validators=[DataRequired()],
                              choices=[('', 'Select'), ('Active', 'Active'), ('Closed', 'Closed')])
    submit = SubmitField('Edit Events')
    
    def validate_editEventVacancy(self, eventVenue):
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
            
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
        facilitySlotsList = []
        for facil in facilDict:
            facils = facilDict.get(facil)
            facilAvailability = facils.get_fac_status()
            if facilAvailability == 'Available':             
                facilityID = facils.get_fac_id()
                facilityIDList.append(facilityID)
                
                facilitySlots = facils.get_fac_slots()
                facilitySlotsList.append(facilitySlots)
                
        eventVenueChosen = self.editEventVenue.data
        eventVacancyChosen = self.editEventVacancy.data
        if eventVenueChosen in facilityIDList:
            index = facilityIDList.index(eventVenueChosen)
            if eventVacancyChosen > facilitySlotsList[index]:
                raise ValidationError(f'Max Event Vacancies is {facilitySlotsList[index]}!')
    
    def validate_editEventDate(self, eventDate): # Dont touch this.
        pre_dateCheck = "%Y-%m-%d"
        dateFormat = "%d%m%y"
        timeFormat = "%H%M%S"
        dateToday = date.today()
        
        startDate = ((self.editEventStartDate.data).strftime(dateFormat) + (self.editEventStartDateTime.data).strftime(timeFormat))
        print(f'Start Date : {startDate}')
        
        endDate = ((self.editEventDate.data).strftime(dateFormat) + (self.editEventDateTime.data).strftime(timeFormat))
        print(f'End Date : {endDate}')
        
        
        if int((self.editEventDate.data).strftime(dateFormat)) < int(dateToday.strftime(dateFormat)): # 300222 < 310122
            raise ValidationError(f"End Date cannot be behind today. Today's Date {dateToday}")
        
        if int(endDate) < int(startDate): # 30122 < 31
            print('Please work man')
            raise ValidationError('End Date cannot be before Start Date')
        
    def validate_editEventStartDate(self, eventStartDate):
        dateFormat = "%d%m%y"
        dateToday = date.today()
                
        if int((self.editEventStartDate.data).strftime(dateFormat)) < int(dateToday.strftime(dateFormat)):
            raise ValidationError(f"End Date cannot be behind today. Today's Date {dateToday}")
        
class eventDeleteForm(FlaskForm):
    deleteEventID = IntegerField('Event ID to delete : ', 
                                 validators=[DataRequired()])
    submit = SubmitField('Delete Events')
    
class eventDeleteForm2(FlaskForm):
    deleteEventID = IntegerField('Event ID to delete : ', 
                                 validators=[DataRequired()],
                                 render_kw={'placeholder' : 'Re-enter ID to delete. (Found in URL)'})
    submit = SubmitField('Delete Events')
    
class eventSignup(FlaskForm):
    eventID = IntegerField('Event ID : ', 
                           validators=[DataRequired()])
    submit = SubmitField('Sign Up')
        
class eventSearchForm(FlaskForm):
    eventSearchItem = StringField('Search : ',
                                  validators=[DataRequired(message='Search input cannot be empty')])
    submit = SubmitField('Search')
    
class eventSortForm(FlaskForm):
    submit = SubmitField('Date (Ascending)')
    
class eventSortFormDescending(FlaskForm):
    submit = SubmitField('Date (Descending)')
    
# Test code

class eventSortMultipleForm(FlaskForm):
    selectData = SelectField('Sort Events',
                             choices=[('Sort Events', 'Sort Events'),
                                      ('sportEvents', 'Sport Events'),
                                      ('lifestyleEvents', 'Lifestyle Events'),
                                      ('otherEvents', 'Other Events'),
                                      ('dateAscending', 'Date (Ascending)'),
                                      ('dateDescending', 'Date (Descending)')])
    submit = SubmitField('Sort Now')
        