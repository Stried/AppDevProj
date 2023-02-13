import random

class FacilityBooking:
     def __init__(self,user,facility,date,timeslot):
          self.__booking_id=""
          self.__user=user
          self.__facility=facility
          self.__date=date
          self.__timeslot=timeslot

     def set_booking_id(self):
          year,month,day=str(self.__date).split("-")
          facility=self.__facility.split("-")[0].strip()
          randomID=""
          for i in range(4): # 4-Digit Random
            randomID+=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
          self.__booking_id=day+month+year+facility+randomID
     
     def set_user(self,user):
          self.__user=user

     def set_facility(self,facility):
          self.__facility=facility

     def set_date(self,date):
          self.__date=date

     def set_timeslot(self,timeslot):
          self.__timeslot=timeslot

     def get_booking_id(self):
          return self.__booking_id
     
     def get_user(self):
          return self.__user

     def get_facility(self):
          return self.__facility

     def get_date(self):
          return self.__date

     def get_timeslot(self):
          return self.__timeslot