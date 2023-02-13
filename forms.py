from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError

import shelve
                
class RegistrationForm(FlaskForm):
    username = StringField('Username : ',
                           render_kw={'placeholder' : 'Username'},
                           validators=[DataRequired(), Length(min = 2, max = 15)])
    firstName = StringField('First Name : ',
                            render_kw={'placeholder' : 'Benjamin'},
                            validators=[DataRequired(), Length(min = 2, max = 15)])
    lastName = StringField('Last Name : ',
                           render_kw={'placeholder' : 'Franklin'},
                           validators=[DataRequired(), Length(min = 2, max = 15)])
    email = StringField('Email : ',
                        render_kw={'placeholder' : 'BenjaminFranklin@example.com'},
                        validators=[DataRequired(), Email()])
    phoneNo = IntegerField('Phone Number : ',
                           render_kw={'placeholder' : '98765432'},
                           validators=[DataRequired(), NumberRange(min=80000000, max=99999999, message='Invalid Phone Number')])
    password = PasswordField('Password : ',
                             validators=[DataRequired(), Length(min = 8, max=30)])
    confirm_password = PasswordField('Confirm Password : ',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        restrictedKWList = ['admin', 'activeplay']
        
        userName = self.username.data
        if not all(letter.isalnum() or letter.isspace() for letter in userName):
            raise ValidationError('No special characters allowed!')
        if userName == 'admin@activeplay.sg' or (userName in restrictedKWList):
            raise ValidationError('Keywords not allowed!')
        
    def validate_firstName(self, firstName):
        restrictedKWList = ['admin', 'activeplay', '.sg']
        
        userFirstName = self.firstName.data
        if not all(letter.isalpha() or letter.isspace() for letter in userFirstName):
            raise ValidationError('No special characters allowed!')
        if userFirstName == 'admin@activeplay.sg' or (userFirstName in restrictedKWList):
            raise ValidationError('Keywords not allowed!')
        
    def validate_lastName(self, lastName):
        restrictedKWList = ['admin', 'activeplay', '.sg']
        
        userLastName = self.lastName.data
        if not all(letter.isalpha() or letter.isspace() for letter in userLastName):
            raise ValidationError('No special characters allowed!')
        if userLastName == 'admin@activeplay.sg' or (userLastName in restrictedKWList):
            raise ValidationError('Keywords not allowed!')
    
    def validate_email(self, userEmail):
        dictUsers = {}
        db = shelve.open('users')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')
            
        userEmail = self.email.data   
        for keys in dictUsers:
            if self.email.data == str(dictUsers[keys].get_email()):
                raise ValidationError('Email already registered.')
        
    def validate_phoneNo(self, userPhoneNo):
        dictUsers = {}
        db = shelve.open('users')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')
            
        for keys in dictUsers:
            if self.phoneNo.data == (dictUsers[keys].get_phoneNo()):
                raise ValidationError('Phone Number already registered.')


class LoginForm(FlaskForm):
    loginField = StringField('Email or Phone Number : ', #label
                        validators=[DataRequired()])
    password = PasswordField('Password : ',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class EditForm(FlaskForm):
    editUsername = StringField('Username : ',
                        render_kw={'placeholder' : 'Username'},
                        validators=[DataRequired(), Length(min = 2, max = 20)])
    editFirstName = StringField('First Name : ',
                            render_kw={'placeholder' : 'Benjamin'},
                            validators=[DataRequired(), Length(min = 2)])
    editLastName = StringField('Last Name : ',
                           render_kw={'placeholder' : 'Franklin'},
                           validators=[DataRequired(), Length(min = 2)])
    editEmail = StringField('Email : ',
                        render_kw={'placeholder' : 'BenjaminFranklin@example.com'},
                        validators=[DataRequired(), Email()])
    editPhoneNo = IntegerField('Phone Number : ',
                               render_kw={'placeholder' : '98765432'},
                               validators=[DataRequired()])


    submit = SubmitField('Update')

class userEditPassword(FlaskForm):
    editPassword = PasswordField('New Password : ',
                            validators=[DataRequired(), Length(min = 8, max=30)])
    editConfirm_password = PasswordField('Confirm New Password : ',
                                     validators=[DataRequired(), EqualTo('editPassword')])
    
    submit = SubmitField('Change Password')

class userSearchForm(FlaskForm):
    userSearchItem = StringField('Search : ',
                                  validators=[DataRequired(message='Search input cannot be empty')])
    submit = SubmitField('Search')
    
class userForgotPasswordCheck(FlaskForm):
    userEmail = StringField('Email : ',
                            render_kw={'placeholder' : 'BenjaminFranklin@example.com'},
                            validators=[Email()])
    submitVerified = SubmitField('Verify')
    
    def validate_userEmail(self, userEmail):
        userCheckList = []
        dictUsers = {}
        db = shelve.open('users')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')
            
        email = self.userEmail.data   
        for i in dictUsers:
            userEmailAdd = dictUsers.get(i).get_email()
            userCheckList.append(userEmailAdd)
            
        print(userCheckList)
        if self.userEmail.data not in userCheckList:
            raise ValidationError('Email not registered.')
    
class userForgotPassword(FlaskForm):
    submit = SubmitField('Submit')
       
class userResetPassword(FlaskForm):
    userPassword = StringField('Password : ',
                               validators=[DataRequired(), Length(min = 8, max=30)])
    userConfirmPassword = PasswordField('Confirm Password : ',
                                        validators=[DataRequired(), EqualTo('userPassword')])
    submitReset = SubmitField('Submit')