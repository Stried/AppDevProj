from flask import Flask, render_template, url_for, flash, redirect, request, session
import shelve
import secrets

from forms import RegistrationForm, LoginForm
from wtforms.validators import ValidationError
from eventForms import eventCreateForm, eventEditForm, eventDeleteForm, eventEditForm2, eventDeleteForm2
from bookingForms import bookingForm, paymentForm
from FacilitiesForms import CreateFacilityForm

from OOP.userFunction import *
from OOP.eventFunction import *
from OOP.Bookings import *
from OOP.Facilities import *


dictUsers = {}
db = shelve.open('users')

try:
    dictUsers = db['Users']
except:
    print('Error in retrieving users from user.db.')
    
    
dictAdmin = {}
db = shelve.open('Admin')

try:
    dictAdmin = db['Admin']
except:
    print('Error in retrieving users from user.db.')
    
# Function def setToAdmin()

user = dictUsers.get(id)

dictAdmin.append(user)
db['Admin'] = dictAdmin

dictUsers.pop(user)
db['Users'] = dictUsers
