import random
import secrets
import shelve
from datetime import date, datetime

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_mail import Mail, Message
from wtforms.validators import ValidationError

from bookingForms import bookingForm, bookingSortForm, paymentForm
from eventForms import *
from FacilitiesForm import (CreateFacilityForm, EditFacilityForm,
                            SearchFacilityForm, SortFacilityForm)
from forms import *
from modules.refreshList import *
from modules.search import *
from modules.sort import *
from OOP.Bookings import *
from OOP.eventFunction import *
from OOP.Facilities import *
from OOP.userFunction import *

# Sets the facilityIDList n facilityUIDList from refreshList.py as a local variable
facilityIDList_App = facilityIDList
facilityUIDList_App = facilityUIDList

app = Flask(__name__)

app.config['SECRET_KEY'] = '8ecce6a32ba6703d10b72f3ccea07175'
app.config["SESSION_PERMANENT"] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'activeplaytest@gmail.com'
app.config['MAIL_PASSWORD'] = 'hfpqlfpnmrrhezau'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Main pages
@app.route('/')
@app.route('/home')
def home():
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)
    
    # Please do not touch this, I really have no clue how to solve this if broken.
    eventSports = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Sports' in events.get_eventType():
            eventSports.append(events)
    
    eventLifestyle = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Lifestyle' in events.get_eventType():
            eventLifestyle.append(events)
        
    eventOthers = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Others' in events.get_eventType():
            eventOthers.append(events)
    
    eventTypeList = ['Sports', 'Lifestyle', 'Others']
    eventTypeDict = {'Sports' : eventSports, 'Lifestyle' : eventLifestyle, 'Others' : eventOthers}
    
    return render_template('index.html', title = 'Home', eventsList = eventsList, eventSports = eventSports, eventLifestyle = eventLifestyle, eventOthers = eventOthers)

@app.route('/contact')
@app.route('/about')
def contact():
    return render_template('forms.html')

@app.route('/mailTest', methods=['GET', 'POST'])
def overview():
    if request.method == 'POST':
         msg = Message('Please Verify Your Email',
                        sender='donotreply@activeplay.sg',
                        recipients=['activeplaytest@gmail.com'])
         msg.body = 'Hello! This is Yue from Activeplay.SG'
         msg.html = '<span>Please verify your account by clicking on this <a href="localhost:5000">link</a></span>'
         
         mail.send(msg)
    return render_template('mailTest.html', title = 'Mail')

# User Functions
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        
        dictUsers = {}
        db = shelve.open('users')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')
            
        userName = form.username.data
        userFirstName = form.firstName.data
        userLastName =  form.lastName.data
        userEmail = form.email.data
        userID = str(User.get_random_UID(User))
        userPhoneNo = form.phoneNo.data
        userDateJoined = (User.get_userJoinDate(User)).strftime("%d/%m/%y")
        userPass = form.password.data
        
        userEmailList = []
        userPhoneNoList = []
        for i in dictUsers:
            userInfo = dictUsers.get(i)
            
            userInfoEmail = userInfo.get_email()
            userEmailList.append(userInfoEmail)
            
            userInfoPhoneNo = userInfo.get_phoneNo()
            userPhoneNoList.append(userInfoPhoneNo)
        
        if form.email.data not in userEmailList and form.phoneNo.data not in userPhoneNoList:
            user = User(userName, userFirstName, userLastName, userEmail, userID, userPhoneNo, userDateJoined, userPass)
            dictUsers[user.get_uid()] = user
            db['Users'] = dictUsers
            
            session['User'] = [userName, userID, userEmail, userFirstName, userLastName, userPhoneNo, userDateJoined]
            
            msg = Message('Please Verify Your Email',
                            sender='donotreply@activeplay.sg',
                            recipients=['activeplaytest@gmail.com'])
            msg.html = f'Hello {userFirstName} {userLastName}! This is Yue from Activeplay.SG. Please verify your account ({userEmail}) by clicking the link <a href="https://127.0.0.1:5000/home">here</a>'
            
            mail.send(msg)
            
            flash(f'A verification email has been sent to {userEmail}.', 'login')
            return redirect(url_for('home'))
    return render_template('registration.html', title = 'Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    dictsUser ={}
    db = shelve.open('users')
    try:
        dictsUser = db['Users']
    except:
        print('Error in User.db test')

    userList = []
    userNameList = []
    userEmailList = []
    userFirstList = []
    userLastList = []
    userPhoneNoList = []
    userDateJoinedList = []
    user48afe0ac895d0a6229298679 = [] # For safety reasons, this isnt called userPassList
    
    for users in dictsUser:
        user = dictsUser.get(users)
        userID = user.get_uid()
        userList.append(userID)

        userName = user.get_username()
        userNameList.append(userName)
        
        userEmail = user.get_email()
        userEmailList.append(userEmail)
        
        userFirst = user.get_firstName()
        userFirstList.append(userFirst)
        
        userLast = user.get_lastName()
        userLastList.append(userLast)
        
        userPhoneNo = user.get_phoneNo()
        userPhoneNoList.append(userPhoneNo)
        
        userDateJoined = user.get_dateJoined()
        userDateJoinedList.append(userDateJoined)
        
        userPass = user.get_password()
        user48afe0ac895d0a6229298679.append(userPass)
    
    try:
        loginPhoneNo = int(form.loginField.data)
        loginEmail = None
    except ValueError:
        loginEmail = form.loginField.data
        loginPhoneNo = None
    except:
        print('Error in logging in.')
            
    if form.validate_on_submit():
        if form.loginField.data == 'admin@activeplay.sg' and form.password.data == 'password':
            flash('You have been logged in as an administrator.', 'login')
            userName = "Administrator"
            userID = '0000000'
            userEmail = 'admin@activeplay.sg'
            userFirst = 'Admin'
            userLast = '-'
            session['User'] = [userName, userID, userEmail, userFirst, userLast]
            return redirect(url_for('home'))
        
        elif loginEmail in userEmailList:
            try:
                index = userEmailList.index(form.loginField.data)
            except:
                flash('Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
                return redirect(url_for('login'))
            
            if form.password.data == user48afe0ac895d0a6229298679[index]:
                userName = userNameList[index] # Item 0
                userID = userList[index] # Item 1
                userEmail = userEmailList[index] # Item 2
                userFirst = userFirstList[index] # Item 3
                userLast = userLastList[index] # Item 4
                userPhoneNo = userPhoneNoList[index] # Item 5
                userDateJoined = userDateJoinedList[index] # Item 6
                session['User'] = [userName, userID, userEmail, userFirst, userLast, userPhoneNo, userDateJoined]
                
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
                return redirect(url_for('login'))
                
        elif loginPhoneNo in userPhoneNoList:
            try:
                index = userPhoneNoList.index(int(form.loginField.data))
            except: 
                flash('Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
                return redirect(url_for('login'))
            
            if form.password.data == user48afe0ac895d0a6229298679[index]:
                userName = userNameList[index] # Item 0
                userID = userList[index] # Item 1
                userEmail = userEmailList[index] # Item 2
                userFirst = userFirstList[index] # Item 3
                userLast = userLastList[index] # Item 4
                userPhoneNo = userPhoneNoList[index] # Item 5
                userDateJoined = userDateJoinedList[index] # Item 6
                session['User'] = [userName, userID, userEmail, userFirst, userLast, userPhoneNo, userDateJoined]

                return redirect(url_for('home'))
            else:
                flash(f'Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
                return redirect(url_for('login'))
                
        else:
            flash('Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
            return redirect(url_for('login'))
        
    return render_template('login.html', title = 'Login', form=form)

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgetPassword():
    forgotPasswordFormCheck = userForgotPasswordCheck()
    forgotPasswordForm = userForgotPassword()
    resetPasswordForm = userResetPassword()
    userList = []         
    
        
    if forgotPasswordFormCheck.validate_on_submit() and forgotPasswordFormCheck.data:
        dictsUser ={}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUser = db['Users']
            else:
                db['Users'] = dictsUser
        except:
            print('An Unknown Error Occured')
        print(dictsUser)
        
        for users in dictsUser:
            user = dictsUser.get(users)
            if user.get_email() == forgotPasswordFormCheck.userEmail.data:
                userPassword = user.get_password()
                userList.append(userPassword)
        
        forgetPasswordMsg = Message('Password Replacement',
                                    sender='donotreply@activeplay.sg',
                                    recipients=['activeplaytest@gmail.com'])
        forgetPasswordMsg.html = f'Hello! This is Yue from Activeplay.SG. <br> Your Password is {userList}. If you did not request a change, please contact support immediately.'
        
        mail.send(forgetPasswordMsg)
        
        flash('Please check your email.', 'resetPassword')
        
    return render_template('forgotPassword.html', title = 'Forgot Password',
                           forgotPasswordFormCheck = forgotPasswordFormCheck,
                           forgotPasswordForm = forgotPasswordForm,
                           userList = userList)

@app.route('/users', methods=['GET', 'POST'])
def users():
    formSearch = userSearchForm()

    if formSearch.validate_on_submit() and request.method == 'POST':
        userSearchData = formSearch.userSearchItem.data
        
        userSearchFunction(userSearchData)
        userUIDList_searchPage = userSearchUIDList # lists from search.py
        userUsernameList_searchPage = userSearchUsernameList
        userFirstNameList_searchPage = userSearchFirstNameList
        userLastNameList_searchPage = userSearchLastNameList
        userEmailList_searchPage = userSearchEmailList
        userPhoneNoList_searchPage = userSearchPhoneNoList
        
        print(userUIDList_searchPage, userUsernameList_searchPage, userFirstNameList_searchPage, userLastNameList_searchPage, userEmailList_searchPage, userPhoneNoList_searchPage)
        
        return render_template('Users/viewUsers.html', formSearch = formSearch,
                               userUIDList_searchPage = userUIDList_searchPage,
                               userUsernameList_searchPage = userUsernameList_searchPage,
                               userFirstNameList_searchPage = userFirstNameList_searchPage,
                               userLastNameList_searchPage = userLastNameList_searchPage,
                               userEmailList_searchPage = userEmailList_searchPage,
                               userPhoneNoList_searchPage = userPhoneNoList_searchPage, 
                               title = userSearchData)
    
    dictsUser ={}
    db = shelve.open('users')
    dictsUser = db['Users']
        
    userList = []
    for users in dictsUser:
        user = dictsUser.get(users)
        userList.append(user)
        
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Users/viewUsers.html', userList = userList, formSearch = formSearch) 
    else:
        return render_template('404.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def editUser(id):
    editForm = EditForm()
    if editForm.validate_on_submit() and request.method == 'POST':
        dictsUser ={}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUser = db['Users']
            else:
                db['Users'] = dictsUser
        except:
            print('An Unknown Error Occured')
        print(dictsUser)
        
        userID = id
        
        currentUser = dictsUser.get(userID)
        currentUserPass = currentUser.get_password()
        
        currentDateJoined = currentUser.get_dateJoined()
        
        userName = editForm.editUsername.data
        userFirst = editForm.editFirstName.data
        userLast = editForm.editLastName.data
        userEmail = editForm.editEmail.data
        userPass = currentUserPass
        userPhoneNo = editForm.editPhoneNo.data
        userDateJoined = currentDateJoined
        print(userID)
        
        
        user = User(userName, userFirst, userLast, userEmail, userID, userPhoneNo, userDateJoined, userPass)
        dictsUser[user.get_uid()] = user
        db['Users'] = dictsUser

        return redirect(url_for('users'))
    
    else:
        dictsUser ={}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUser = db['Users']
            else:
                db['Users'] = dictsUser
        except:
            print('An Unknown Error Occured')
        print(dictsUser)
        
        users = dictsUser.get(id)
        editForm.editUsername.data = users.get_username()
        editForm.editFirstName.data = users.get_firstName()
        editForm.editLastName.data = users.get_lastName()
        editForm.editEmail.data = users.get_email()
        editForm.editPhoneNo.data = users.get_phoneNo()
        
        
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Users/userEdit.html', editForm = editForm)
    else:
        return render_template('404.html')

@app.route('/delete/<id>', methods=['GET', 'POST'])
def deleteUser(id):
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        dictsUsers = {}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUsers = db['Users']
            else:
                db['Users'] = dictsUsers
        except:
            print('An Unknown Error Occured.')
            
        userID = id
        dictsUsers.pop(userID)
        db['Users'] = dictsUsers
        
        return redirect(url_for('users'))
    else:
        return render_template('404.html')

@app.route('/account/changeDetails/<id>', methods=["GET", "POST"])
def changeUserDetails(id):
    editForm = EditForm()
    if editForm.validate_on_submit() and request.method == 'POST':
        dictsUser ={}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUser = db['Users']
            else:
                db['Users'] = dictsUser
        except:
            print('An Unknown Error Occured')
        print(dictsUser)
        
        userID = id
        
        currentUser = dictsUser.get(userID)
        currentUserPass = currentUser.get_password()
        
        currentDateJoined = currentUser.get_dateJoined()
        
        userName = editForm.editUsername.data
        userFirst = editForm.editFirstName.data
        userLast = editForm.editLastName.data
        userEmail = editForm.editEmail.data
        userPass = currentUserPass
        userPhoneNo = editForm.editPhoneNo.data
        userDateJoined = currentDateJoined
        print(userID)
        
        
        user = User(userName, userFirst, userLast, userEmail, userID, userPhoneNo, userDateJoined, userPass)
        dictsUser[user.get_uid()] = user
        db['Users'] = dictsUser
        
        session.pop('User', None)
        session['User'] = [userName, userID, userEmail, userFirst, userLast, userPhoneNo, userDateJoined]

        return redirect(url_for('account'))
    
    else:
        dictsUser ={}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUser = db['Users']
            else:
                db['Users'] = dictsUser
        except:
            print('An Unknown Error Occured')
        print(dictsUser)
        print(id)
        
        users = dictsUser.get(id)
        editForm.editUsername.data = users.get_username()
        editForm.editFirstName.data = users.get_firstName()
        editForm.editLastName.data = users.get_lastName()
        editForm.editEmail.data = users.get_email()
        editForm.editPhoneNo.data = users.get_phoneNo()
        
    return render_template('Users/userChangeDetails.html', editForm = editForm)

@app.route('/account/changePassword/<id>', methods=["GET", "POST"])
def changeUserPassword(id):
    editForm = userEditPassword()
    
    if editForm.validate_on_submit() and request.method == 'POST':
        dictsUser ={}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUser = db['Users']
            else:
                db['Users'] = dictsUser
        except:
            print('An Unknown Error Occured')
        print(dictsUser)
        
        userID = id
        
        currentUser = dictsUser.get(userID)
        currentUserPass = currentUser.get_password()
        currentDateJoined = currentUser.get_dateJoined()
        
        userName = currentUser.get_username()
        userFirst = currentUser.get_firstName()
        userLast = currentUser.get_lastName()
        userEmail = currentUser.get_email()
        userPass = currentUserPass
        userPhoneNo = currentUser.get_phoneNo()
        userDateJoined = currentDateJoined
        userPassword = editForm.editPassword.data
        print(userID)
        
        if userPassword == userPass:
            flash('New password cannot be the same as old password')
            return render_template('Users/userChangePassword.html', editForm=editForm)
        
        user = User(userName, userFirst, userLast, userEmail, userID, userPhoneNo, userDateJoined, userPassword)
        dictsUser[user.get_uid()] = user
        db['Users'] = dictsUser
        
        return redirect(url_for('home'))
    return render_template('Users/userChangePassword.html', editForm = editForm)

# DO NOT TOUCH, NO CLUE WHY IT WORKS, IT JUST DOES - WE DON'T KNOW HOW EITHER - CONSULT BUDDHA @ 404
@app.route('/account', methods=['GET', 'POST'])
def account():
    form = LoginForm()
    if request.method == 'POST':
        return render_template('Users/userAccount.html', user = session['User'][0]) # TODO: Change how the url looks
    else:
        return redirect(url_for('home'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('User', None)
    session.pop('UserID', None)
    return redirect(url_for('home'))

@app.route('/admin')
def adminWorkspace():
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Users/adminWorkspace.html') 
    else:
        return render_template('404.html')

# Event Functions


@app.route('/events/createEvents', methods=['GET', 'POST'])
def createEvent():
    refreshFacilityList()
    facilityIDList_createEvent = facilityIDList_App
    facilityUIDList_createEvent = facilityUIDList_App
    
    formEvents = eventCreateForm()
    # Before Form Submission
    formEvents.eventVenue.choices = [(facilityIDList_createEvent[i], f"{facilityUIDList_createEvent[i]} - {facilityIDList_createEvent[i]}") for i in range(len(facilityUIDList_createEvent))] # refreshes the facility list
    
    facilDict = {}
    facilDB = shelve.open('Facilities')
    try:    
        if 'Facilities' in facilDB:
            facilDict = facilDB['Facilities']
        else:
            facilDB['Facilities'] = facilDict
    except:
        print('Error in retrieving facilities.')
            
    eventLocationDict = {}
    eventLocationDB = shelve.open('tempEventLocation')
    try:
        if 'location' in eventLocationDB:
            eventLocationDict = eventLocationDB['location']
        else:
            eventLocationDB['location'] = eventLocationDict
    except:
        print('Location not found.')
        
    facilityLocationList = []
    for events in eventLocationDict:
        event = eventLocationDict.get(events)
        eventLoc = event[0]
        for facility in facilDict:
            facilityLocation = facility.get_fac_loc()
            if facilityLocation == eventLoc:
                facilityLocationList.append(facility)
    print(facilityLocationList)
            
    if formEvents.validate_on_submit() and request.method == 'POST':  
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
    
                     
        eventName = formEvents.eventName.data
        eventDesc = formEvents.eventDesc.data
        eventVacancy = formEvents.eventVacancy.data
        eventDate = formEvents.eventDate.data
        eventDateTime = formEvents.eventDateTime.data
        eventStartDate = formEvents.eventStartDate.data
        eventStartDateTime = formEvents.eventStartDateTime.data
        eventID = formEvents.eventID.data
        eventType = formEvents.eventType.data
        eventLocation = formEvents.eventLocation.data        
        eventVenue = formEvents.eventVenue.data
        eventStatus = formEvents.eventStatus.data    
            
        ce = createEvents(eventName, eventDesc, eventVacancy, eventDate, eventDateTime, eventStartDate, eventStartDateTime, eventID, eventType, eventLocation, eventVenue, eventStatus)
        eventsDict[ce.get_eventID()] = ce
        eventDB['Events'] = eventsDict
        
        return redirect(url_for('eventsPage'))
    
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Events/eventCreate.html', formEvents=formEvents)   
    else:
        return render_template('404.html') 

# EDIT EVENTS ROUTING
    # DO NOT TOUCH!!!!!!!!

@app.route('/events/editEvents/<int:id>', methods=['GET', 'POST'])
def editEventDirect(id):
    refreshFacilityList()
    
    facilityIDList_editEvent = facilityIDList_App
    facilityUIDList_editEvent = facilityUIDList_App
    # DO NOT TOUCH!!!!!!!!
    formEvents = eventEditForm2()
    formEvents.editEventVenue.choices = [(facilityIDList_editEvent[i], f"{facilityUIDList_editEvent[i]} - {facilityIDList_editEvent[i]}") for i in range(len(facilityUIDList_editEvent))] # refreshes the facility list
    
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
    for facil in facilDict:
        facils = facilDict.get(facil)
        facilAvailability = facils.get_fac_status()
        if facilAvailability == 'Available':
            facilityUID = facils.get_uniqueID()
            facilityUIDList.append(facilityUID)
            facilityID = facils.get_fac_id()
            facilityIDList.append(facilityID)
            
    if formEvents.validate_on_submit() and request.method == 'POST':
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
        
        eventName = formEvents.editEventName.data
        eventDesc = formEvents.editEventDesc.data
        eventVacancy = formEvents.editEventVacancy.data
        eventDate = formEvents.editEventDate.data
        eventDateTime = formEvents.editEventStartDateTime.data
        eventStartDate = formEvents.editEventStartDate.data
        eventStartDateTime = formEvents.editEventStartDateTime.data
        eventID = id
        eventType = formEvents.editEventType.data
        eventLocation = formEvents.editEventLocation.data
        eventVenue = formEvents.editEventVenue.data
        eventStatus = formEvents.editEventStatus.data
        
        if eventID not in eventsDict.keys():
            print('Error.')
            flash('Event ID not found in Event Database.', 'error')
        else:
            ce = createEvents(eventName, eventDesc, eventVacancy, eventDate, eventDateTime, eventStartDate, eventStartDateTime, eventID, eventType, eventLocation, eventVenue, eventStatus)
            eventsDict[ce.get_eventID()] = ce
            eventDB['Events'] = eventsDict
            
            eventDB.close()
            print(eventsDict.keys())
                    
            return redirect(url_for('eventsPage'))
        
    else:
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
        
        print(eventsDict)
        event = eventsDict.get(id)
        print(event)
        formEvents.editEventName.data = event.get_eventName()
        formEvents.editEventDesc.data = event.get_eventDesc()
        formEvents.editEventVacancy.data = event.get_eventVacancy()
        formEvents.editEventDate.data = event.get_eventDate()
        formEvents.editEventDateTime.data = event.get_eventDateTime()
        formEvents.editEventStartDate.data = event.get_eventStartDate()
        formEvents.editEventStartDateTime.data = event.get_eventStartDateTime()
        formEvents.editEventType.data = event.get_eventType()
        formEvents.editEventLocation.data = event.get_eventLocation()
        formEvents.editEventVenue.data = event.get_eventVenue()
        formEvents.editEventStatus.data = event.get_eventStatus()
        
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Events/eventEditDirect.html', formEvents = formEvents)
    else:
        return render_template('404.html')

@app.route('/events/deleteEvents/<int:id>', methods=['GET', 'POST'])
def deleteEventDirect(id):
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        eventDB = shelve.open('Events')
        eventsDict = {}
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
        eventID = id

        eventsDict.pop(eventID)  
        eventDB['Events'] = eventsDict  
        return redirect(url_for('eventsPage'))
    else:
        return render_template('404.html')

@app.route('/events', methods=['GET', 'POST'])
def eventsPage():
    formSearch = eventSearchForm()
    formSort = eventSortMultipleForm()
    
    if formSearch.validate_on_submit() and request.method == 'POST':
        eventSearchData = formSearch.eventSearchItem.data
        
        eventSearchFunction(eventSearchData)
        
        eventIDList_searchPage = eventSearchIDList # lists from search.py
        eventNameList_searchPage = eventSearchNameList
        eventLocationList_searchPage = eventSearchLocationList
        eventVenueList_searchPage = eventSearchVenueList
        
        print(eventIDList_searchPage, eventNameList_searchPage, eventLocationList_searchPage, eventVenueList_searchPage)
        
        return render_template('Events/eventMain.html', formSearch = formSearch,
                               eventIDList_searchPage = eventIDList_searchPage,
                               eventNameList_searchPage = eventNameList_searchPage,
                               eventLocationList_searchPage = eventLocationList_searchPage,
                               eventVenueList_searchPage = eventVenueList_searchPage,
                               formSort = formSort,
                               title = eventSearchData)
    
    if formSort.validate_on_submit() and request.method == "POST":
        formSortData = formSort.selectData.data
        
        if formSortData == 'sportEvents':
            eventSortBySport()
            eventSportsList_App = eventSportsList
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventSportsListDisplay = eventSportsList_App,
                                   title = "Sports")
            
        elif formSortData == 'lifestyleEvents':
            eventSortByLifestyle()
            eventLifestyleList_App = eventLifestyleList
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventLifestyleListDisplay = eventLifestyleList_App,
                                   title = "Lifestyle")
            
        elif formSortData == 'otherEvents':
            eventSortByOthers()
            eventOthersList_App = eventOthersList
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventOthersListDisplay = eventOthersList_App,
                                   title = "Others")
            
        elif formSortData == 'dateAscending':
            eventSortByTimeAscending()
            eventTimeList = eventListFinalSort
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventTimeList = eventTimeList,
                                   title = "Date (Ascending)")
            
        elif formSortData == 'dateDescending':
            eventSortByTimeDescending()
            eventTimeListDescending = eventListFinalSortDescending
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventTimeListDescending = eventTimeListDescending,
                                   title = "Date (Descending)")
        
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)
    print(eventsList)
        
    eventSignUp = []
    eventSignUpDict = {}
    eventSignUpDB = shelve.open('eventSignUp')
    try:
        if 'eventSignUp' in eventSignUpDB:
            eventSignUpDict = eventSignUpDB['eventSignUp']
        else:
            eventSignUpDB['eventSignUp'] = eventSignUpDict
    except:
        print('An Unknown Error Occured.')
    
    eventSignUp = eventSignUpDict
    print(eventSignUp)
            
    return render_template('Events/eventMain.html', eventsList = eventsList,
                           formSort = formSort,
                           formSearch = formSearch)

@app.route('/events/signup/<int:id>', methods=['GET', 'POST'])
def eventSignup(id):
    eventSignUpList = []
    eventSignUpDB = shelve.open('eventSignUp')
    eventSignUpDict = {}
    
    # list the userID under the event ID, find users registered to the event not event registered to the user
    eventID = id
    if 'User' in session:
        userID = session['User'][1]

        try:
            if 'eventSignUp' in eventSignUpDB:
                eventSignUpDict = eventSignUpDB['eventSignUp']
            else:
                eventSignUpDB['eventSignUp'] = eventSignUpDict
        except:
            print('An Unknown Error Occured.')
            
        # Check whether event key already in dictionary
        if eventID in eventSignUpDict.keys():
            eventList = []
            
            for events in eventSignUpDict[eventID]: # list = [1, 2, 3, 4, 5, 6]
                eventList.append(events)
                
            if userID not in eventList:
                eventList.append(userID)
                print(eventList)
                eventSignUpDict[eventID] = eventList
                
                eventSignUpDB['eventSignUp'] = eventSignUpDict
            else:
                print('User already registered!')
        else:
            eventSignUpList.append(userID)
            eventSignUpDict[eventID] = eventSignUpList
            eventSignUpDB['eventSignUp'] = eventSignUpDict
            
        return redirect(url_for('eventsPage'))
    else:
        return redirect(url_for('login'))

@app.route('/events/registered', methods=['GET', 'POST'])
def eventRegistered():
    if 'User' in session:
        userID = session['User'][1]
        eventSignUpDB = shelve.open('eventSignUp')
        eventSignUpDict = {}
        
        try:
            if 'eventSignUp' in eventSignUpDB:
                eventSignUpDict = eventSignUpDB['eventSignUp']
            else:
                eventSignUpDB['eventSignUp'] = eventSignUpDict
        except:
            print('An Unknown Error Occured.')

        userRegisteredList = []
        for events in eventSignUpDict:
            if userID in eventSignUpDict[events]:
                userRegisteredList.append(events)
        print(userRegisteredList)
        
        eventsDict = {}
        eventDB = shelve.open('Events')
        eventsDict = eventDB['Events']

        eventInfoID = []
        eventInfoName = []
        eventDisplayName = []
        eventInfoType = []
        eventDisplayType = []
        
        for i in eventsDict:
            eventID = eventsDict[i].get_eventID()
            print(eventID)
            eventInfoID.append(eventID)
            eventName = eventsDict[i].get_eventName()
            print(eventName)
            eventInfoName.append(eventName)
            eventType = eventsDict[i].get_eventType()
            eventInfoType.append(eventType)
        
        for id in userRegisteredList:
            index = eventInfoID.index(id)
            eventNameIndex = eventInfoName[index]
            eventDisplayName.append(eventNameIndex)
            
            eventTypeIndex = eventInfoType[index]
            eventDisplayType.append(eventTypeIndex)
        
        print(eventDisplayName)
        return render_template('Events/eventRegistered.html', registeredEventList = userRegisteredList, registeredEventName = eventDisplayName, registeredEventType = eventDisplayType)
    else:
        return redirect(url_for('login'))

# Booking functions
@app.route('/booking', methods=['GET', 'POST'])
def bookingPage():
    formsBooking = bookingForm()
    refreshFacilityList()
    facilityIDList_createBooking = facilityIDList_App
    facilityUIDList_createBooking = facilityUIDList_App
    #Then hpw do I do all facilities for sorting, can try
    formsBooking.bookingFacilityID.choices = [(facilityIDList_createBooking[i], f"{facilityUIDList_createBooking[i]} - {facilityIDList_createBooking[i]}") for i in range(len(facilityUIDList_createBooking))] # refreshes the facility list
    
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
    for facil in facilDict:
        facils = facilDict.get(facil)
        facilAvailability = facils.get_fac_status()
        if facilAvailability == 'Available':
            facilityUID = facils.get_uniqueID()
            facilityUIDList.append(facilityUID)
            facilityID = facils.get_fac_id()
            facilityIDList.append(facilityUID)

    bookingFacilDict = {}
    bookingFacilDB = shelve.open('BookingFacil')
    try:
        if 'BookingFacil' in bookingFacilDB:
            bookingFacilDict = bookingFacilDB['BookingFacil']
        else:
            bookingFacilDB['BookingFacil'] = bookingFacilDict
    except:
        print('Error in retrieving bookings.')
                
    if 'User' in session:
        userID = session['User'][1]
        if formsBooking.validate_on_submit() and request.method == 'POST':
            bookFacil = formsBooking.bookingFacilityID.data                    
            bookDate = formsBooking.bookingDate.data                   
            bookTime = formsBooking.bookingTimeSlot.data
            conflict=False           

            for i in bookingFacilDict:
                other_booking=bookingFacilDict[i]
                if other_booking.get_facility()==bookFacil and other_booking.get_date()==bookDate and other_booking.get_timeslot()==bookTime:
                    conflict=True

            if conflict==False:
                for facil in facilDict:
                    if facilDict[facil].get_fac_id()==bookFacil:
                        cost = facilDict[facil].get_fac_rate()
                return redirect(url_for('bookingPayment', userID = userID, bookFacil = bookFacil, bookDate = bookDate, bookTime = bookTime, cost = cost))

            else:
                return render_template('Booking/bookingConflict.html', formsBooking = formsBooking, text = "Facility Booking")
        
        return render_template('Booking/bookingMain.html', formsBooking = formsBooking)
       
    else:
        return redirect(url_for('login'))

@app.route('/booking/bookingPayment/<userID>/<bookFacil>/<bookDate>/<bookTime>/<cost>', methods=['GET', 'POST'])
def bookingPayment(userID, bookFacil, bookDate, bookTime, cost):
    formsPayment = paymentForm()
    if formsPayment.validate_on_submit() and request.method == 'POST':
        payMethod = formsPayment.paymentMethod.data
        cardNum = formsPayment.cardNumber.data
        expireDate = formsPayment.expirationDate.data
        securePIN = formsPayment.securityPIN.data

        bookingFacilDict = {}
        bookingFacilDB = shelve.open('BookingFacil')
        try:
            if 'BookingFacil' in bookingFacilDB:
                bookingFacilDict = bookingFacilDB['BookingFacil']
            else:
                bookingFacilDB['BookingFacil'] = bookingFacilDict
        except:
            print('Error in retrieving bookings.')
        
        bookDate = bookDate.replace("-","/")
        bookDate = datetime.datetime.strptime(bookDate, '%Y/%m/%d').date()
        fb = FacilityBooking(userID, bookFacil, bookDate, bookTime)
        fb.set_booking_id()
        bookingUID = fb.get_booking_id()
        bookingFacilDict[(bookingUID)] = fb
        bookingFacilDB['BookingFacil'] = bookingFacilDict
        bookingFacilDB.close()

        if 'User' in session:
            userID = session['User'][1]
            bookingsDict = {}
            bookingDB = shelve.open('Bookings')
            try:
                if 'Bookings' in bookingDB:
                    bookingsDict = bookingDB['Bookings']
                else:
                    bookingDB['Bookings'] = bookingsDict
            except:
                print('Error in retrieving bookings')
            
            bookingsDict[(bookingUID)] = fb
            bookingDB['Bookings'] = bookingsDict
            bookingDB.close()
            
            return redirect(url_for('bookingCurrent'))

    return render_template('Booking/bookingPayment.html', formsPayment = formsPayment, cost = cost)

@app.route('/booking/bookingCurrent', methods=['GET', 'POST'])
def bookingCurrent():
    refreshFacilityList()
    facilityIDList_createBooking = facilityIDList_App
    facilityUIDList_createBooking = facilityUIDList_App
    formsBookingSort = bookingSortForm()
    
    formsBookingSort.selectData.choices = [(facilityIDList_createBooking[i], f"{facilityUIDList_createBooking[i]} - {facilityIDList_createBooking[i]}") for i in range(len(facilityUIDList_createBooking))] # refreshes the facility list
    if 'User' in session:
        userID = session['User'][1]
        bookingsDict = {}
        bookingDB = shelve.open('Bookings')
        bookingsDict = bookingDB['Bookings']
    
        bookingsList=[]
        for booking in bookingsDict:
            bookings = bookingsDict[booking]
            if bookings.get_user()==userID and bookings.get_date()>=date.today():
                if formsBookingSort.validate_on_submit() and request.method == "POST":
                    sortData = formsBookingSort.selectData.data
                    if bookings.get_facility()==sortData:
                        bookingsList.append(bookings)
                else:
                    bookingsList.append(bookings)

        return render_template('Booking/bookingCurrent.html', bookingsList = bookingsList, formsBookingSort = formsBookingSort)
    else:
        return redirect(url_for('login'))

@app.route('/booking/bookingEdit/<id>', methods=['GET', 'POST'])
def editBookings(id):
    refreshFacilityList()
    facilityIDList_createBooking = facilityIDList_App
    facilityUIDList_createBooking = facilityUIDList_App
    formsBooking = bookingForm()
    formsBooking.bookingFacilityID.choices = [(facilityIDList_createBooking[i], f"{facilityUIDList_createBooking[i]} - {facilityIDList_createBooking[i]}") for i in range(len(facilityUIDList_createBooking))] # refreshes the facility list

    if formsBooking.validate_on_submit() and request.method == 'POST':
        bookingsDict = {}
        bookingDB = shelve.open('Bookings')
        try:
            if 'Bookings' in bookingDB:
                bookingsDict = bookingDB['Bookings']
            else:
                bookingDB['Bookings'] = bookingsDict
        except:
            print('Error in retrieving bookings.')

        bookingFacilDict = {}
        bookingFacilDB = shelve.open('BookingFacil')
        try:
            if 'BookingFacil' in bookingFacilDB:
                bookingFacilDict = bookingFacilDB['BookingFacil']
            else:
                bookingFacilDB['BookingFacil'] = bookingFacilDict
        except:
            print('Error in retrieving bookings.')

        bookFacil = formsBooking.bookingFacilityID.data
        bookDate = formsBooking.bookingDate.data
        bookTime = formsBooking.bookingTimeSlot.data
        conflict = False
        
        for i in bookingFacilDict:
            other_booking=bookingFacilDict[i]
            if other_booking.get_facility()==bookFacil and other_booking.get_date()==bookDate and other_booking.get_timeslot()==bookTime:
                conflict=True

        if conflict==False:
            fb = bookingsDict[id]
            fb.set_facility(bookFacil)
            fb.set_date(bookDate)
            fb.set_timeslot(bookTime)
            bookingsDict[fb.get_booking_id()] = fb
            bookingDB['Bookings'] = bookingsDict
            bookingFacilDict[fb.get_booking_id()] = fb
            bookingFacilDB['BookingFacil'] = bookingsDict

            bookingDB.close()
            bookingFacilDB.close()
        
            return redirect(url_for('bookingCurrent'))

        else:
            return render_template('Booking/bookingConflict.html', formsBooking = formsBooking, text = "Edit Bookings")
    else:
        bookingsDict = {}
        bookingDB = shelve.open('Bookings')
        try:
            if 'Bookings' in bookingDB:
                bookingsDict = bookingDB['Bookings']
            else:
                bookingDB['Bookings'] = bookingsDict
        except:
            print('Error in retrieving bookings.')
            
        booking = bookingsDict.get(id)
        formsBooking.bookingFacilityID.data = booking.get_facility()
        formsBooking.bookingDate.data = booking.get_date()
        formsBooking.bookingTimeSlot.data = booking.get_timeslot()

        
    return render_template('Booking/bookingEdit.html', formsBooking = formsBooking)

@app.route('/booking/deleteBooking/<id>', methods=['GET', 'POST'])
def deleteBookings(id):
    bookingsDict = {}
    bookingDB = shelve.open('Bookings')
    try:
        if 'Bookings' in bookingDB:
            bookingsDict = bookingDB['Bookings']
        else:
            bookingDB['Bookings'] = bookingsDict
    except:
        print('Error in retrieving bookings.')

    bookingFacilDict = {}
    bookingFacilDB = shelve.open('BookingFacil')
    try:
        if 'BookingFacil' in bookingFacilDB:
            bookingFacilDict = bookingFacilDB['BookingFacil']
        else:
            bookingFacilDB['BookingFacil'] = bookingFacilDict
    except:
        print('Error in retrieving bookings.')

    bookingsDict.pop(id)
    bookingDB['Bookings'] = bookingsDict
    bookingFacilDict.pop(id)
    bookingFacilDB['BookingFacil'] = bookingFacilDict

    bookingDB.close()
    bookingFacilDB.close()

    return redirect(url_for('bookingCurrent'))

@app.route('/booking/bookingHistory', methods=['GET', 'POST'])
def bookingHistory():
    refreshFacilityList()
    facilityIDList_createBooking = facilityIDList_App
    facilityUIDList_createBooking = facilityUIDList_App
    formsBookingSort = bookingSortForm()
    
    formsBookingSort.selectData.choices = [(facilityIDList_createBooking[i], f"{facilityUIDList_createBooking[i]} - {facilityIDList_createBooking[i]}") for i in range(len(facilityUIDList_createBooking))] # refreshes the facility list
    
    if 'User' in session:
        userID = session['User'][1]
        bookingsDict = {}
        bookingDB = shelve.open('Bookings')
        bookingsDict = bookingDB['Bookings']
        
        bookingsList=[]
        for booking in bookingsDict:
            bookings = bookingsDict.get(booking)
            if bookings.get_user()==userID:
                if formsBookingSort.validate_on_submit() and request.method == "POST":
                    sortData = formsBookingSort.selectData.data
                    if bookings.get_facility()==sortData:
                        bookingsList.append(bookings)
                else:
                    bookingsList.append(bookings)

        return render_template('Booking/bookingHistory.html', bookingsList = bookingsList, formsBookingSort = formsBookingSort)
    else:
        return redirect(url_for('login'))

@app.route('/facilities', methods=['GET', 'POST'])
def facilitiesPage(): #didnt realize the tepmplete lmao
    FacilityFormSearch = SearchFacilityForm()
    facilityFormSort = SortFacilityForm()

    if FacilityFormSearch.validate_on_submit() and request.method == 'POST':
        facilitySearchData = FacilityFormSearch.facilitySearchItem.data

        facilitySearchFunction(facilitySearchData)

        facilityIDList_searchPage = facilitySearchIDList
        facilityFac_IDList_searchPage = facilitySearchFac_IDList
        facilityLocationList_searchPage = facilitySearchLocationList
        facilitySlotsList_searchPage = facilitySearchSlotsList

        print(facilityIDList_searchPage,
              facilityFac_IDList_searchPage,
              facilityLocationList_searchPage,
              facilitySlotsList_searchPage)

        return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch,
                               facilityFormSort = facilityFormSort,
                               facilIDList_searchPage = facilityIDList_searchPage,
                               facilFacilityIDList_searchPage = facilityFac_IDList_searchPage,
                               facilLocationList_searchPage = facilityLocationList_searchPage, 
                               facilitySlotsList_searchPage = facilitySlotsList_searchPage,
                               title = facilitySearchData) 

    if facilityFormSort.validate_on_submit() and request.method == "POST":
        sortData = facilityFormSort.facilitySortItem.data
        
        if sortData == 'angMoKio':
            facilitySortAMK()
            facilityListAMK_App = facilityAMKList
            
            return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch,
                                   facilityFormSort = facilityFormSort,
                                   facilityListAMKDisplay = facilityListAMK_App,
                                   title = "Ang Mo Kio")
            
        elif sortData == 'hougang':
            facilitySortHG()
            facilityListHG_App = facilityHGList
            
            return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch,
                                    facilityFormSort = facilityFormSort,
                                    facilityListHGDisplay = facilityListHG_App,
                                    title = 'Hougang')
            
        elif sortData == 'macpherson':
            facilitySortMP()
            facilityListMP_App = facilityMPList
            
            return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch,
                                    facilityFormSort = facilityFormSort,
                                    facilityListMPDisplay = facilityListMP_App,
                                    title = "Macpherson")
        
        elif sortData == 'braddell':
            facilitySortBD()
            facilityListBD_App = facilityBDList
            
            return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch,
                                    facilityFormSort = facilityFormSort,
                                    facilityListBDDisplay = facilityListBD_App,
                                    title = "Braddell")
            
        elif sortData == 'seletar':
            facilitySortSL()
            facilityListSL_App = facilitySLList
            
            return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch,
                                    facilityFormSort = facilityFormSort,
                                    facilityListSLDisplay = facilityListSL_App,
                                    title = "Seletar")

        elif sortData == 'goldenMile':
            facilitySortGM()
            facilityListGM_App = facilityGMList
            
            return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch,  
                                    facilityFormSort = facilityFormSort,
                                    facilityListGMDisplay = facilityListGM_App,
                                    title = "Golden Mile")
           
    facilDict = {}
    facilDB = shelve.open('Facilities')
    facilDict = facilDB['Facilities']
    print(facilDict)
    
    facilList = []
    for facil in facilDict:
        facilities = facilDict.get(facil)
        facilList.append(facilities)
    print(facilList)
        
    facilLoc = ['Ang Mo Kio', 'Hougang', 'Macpherson', 'Braddell', 'Seletar', 'Golden Mile']
    
    return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch, facilityFormSort = facilityFormSort, facilList = facilList, facilLoc = facilLoc)

@app.route('/facilities/facilitiesCreate', methods=['GET', 'POST'])
def createFacilities():
    formsFacil = CreateFacilityForm()
    facilDict = {}
    facilDB = shelve.open('Facilities')
    if formsFacil.validate_on_submit() and request.method == 'POST':   
        try:    
            if 'Facilities' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilities'] = facilDict
        except:
            print('Error in retrieving facilities.')
        # oy alan who lives in a pineapple under the sea
        facilLocation = formsFacil.facility_location.data
        location = facilLocation
        
        facilType = formsFacil.facility_type.data
        type = facilType

        facilID = (str(formsFacil.facility_id.data) + " - " + str(type)) # Hougang Stadium - 53, Sengkang Stadium - 54BD01 - 06
        facilStatus = formsFacil.facility_status.data
        facilSlots = formsFacil.facility_slots.data
        facilRates = ("%.2f" % float(formsFacil.facility_rates.data))

        uniqueID = len(facilDict)
        uniqueID += 1
        uniqueIDCheckList = []
        for i in facilDict:
            uniqueIDCheck = facilDict.get(i)
            uniqueIDCheckList.append(uniqueIDCheck)
            
        if uniqueID in uniqueIDCheckList:
            uniqueID += 1
        
        facil = Facilities(facilID, facilStatus, facilSlots, facilLocation, facilRates ,facilType, uniqueID)
        facilDict[facil.get_uniqueID()] = facil # get id
        facilDB['Facilities'] = facilDict
        
        facilDB.close()
        return redirect(url_for('facilitiesPage'))
    
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Facilities/facilitiesCreate.html', formsFacil = formsFacil)
    else:
        return render_template('404.html')

@app.route('/facilities/facilitiesEdit/<int:id>', methods=['GET', 'POST'])
def editFacilities2(id):
    formsFacil = EditFacilityForm()
    facilDict = {}
    facilDB = shelve.open('Facilities')
    if formsFacil.validate_on_submit() and request.method == 'POST':  
        try:    
            if 'Facilities' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilities'] = facilDict
        except:
            print('Error in retrieving Facilities.')
        
        facilLocation = formsFacil.edit_facility_location.data
        location = facilLocation
        
        facilType = formsFacil.edit_facility_type.data
        type = facilType
        
        facilID = str(formsFacil.edit_facility_id.data) # Hougang Stadium - 53, Sengkang Stadium - 54BD01 - 06
        facilStatus = formsFacil.edit_facility_status.data
        facilSlots = formsFacil.edit_facility_slots.data
        facilRates = ("%.2f" % float(formsFacil.edit_facility_rates.data))
        
        facil = Facilities(facilID, facilStatus, facilSlots, facilLocation, facilRates, facilType, id)
        facilDict[id] = facil  
        facilDB['Facilities'] = facilDict
        
        facilDB.close()
        return redirect(url_for('facilitiesPage'))
    
    else:
        facilDict = {}
        facilDB = shelve.open('Facilities')
        try:    
            if 'Facilities' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilities'] = facilDict
        except:
            print('Error in retrieving Facilities.')
        
        id = int(id)
        if id in facilDict:
            facility = facilDict.get(id)
            print(facility)
            formsFacil.edit_facility_id.data = facility.get_fac_id()
            formsFacil.edit_facility_location.data = facility.get_fac_loc()
            formsFacil.edit_facility_slots.data = facility.get_fac_slots()
            formsFacil.edit_facility_status.data = facility.get_fac_status()
            formsFacil.edit_facility_type.data = facility.get_fac_amt()
            formsFacil.edit_facility_rates.data = facility.get_fac_rate()
            
        else:
            print('An Error Is Here')
    
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Facilities/facilitiesEdit.html', formsFacil = formsFacil)
    else:
        return render_template('404.html')

@app.route('/facilities/facilitiesDelete/<id>', methods=['GET', 'POST'])
def deleteFacilitiesDirect(id):
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        facilDB = shelve.open('Facilities')
        facilDict = {}
        try:
            if 'Facilities' in facilDB:
                facilDict = facilDB['Facilities'] 
            else:
                facilDB['Facilities'] = facilDict
        except:
            print('Error in retrieving Facilities.')
        facilID = int(id)

        facilDict.pop(facilID)  
        facilDB['Facilities'] = facilDict  
        return redirect(url_for('facilitiesPage'))
    else:
        return render_template('404.html')\

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
# 723rd line :D
# 17Jan2023 - No longer is this the 723rd line, we have gone too far off. (1089th line)
# 25/1/2023 - It's only been 8 days..., we gone further (1207th line)
# 27Jan2023 - It's only getting longer. When will our suffering end? (1265th Line)
# 1Feb2023 - It's only geting loonger..... When can i retire? - Alan (1376th Line)
# 10Feb2023 - THE SORT FUNCTION IS WORKING WHEEEEEEE - Alan (1584th Line)
# 11Feb2023 - Removed so many lines of code damn
# 12Feb2023 - 1368th Line. We're optimizing!