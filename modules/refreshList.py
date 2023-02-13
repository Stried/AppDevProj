import shelve

from OOP.userFunction import *
from OOP.eventFunction import *
from OOP.Bookings import *
from OOP.Facilities import *

facilityIDList = []
facilityUIDList = []

def refreshFacilityList():
    global facilityIDList
    global facilityUIDList
    
    facilityIDList.clear()
    facilityUIDList.clear()
    
    facilDict = {}
    facilDB = shelve.open('Facilities')
    try:    
        if 'Facilities' in facilDB:
            facilDict = facilDB['Facilities']
        else:
            facilDB['Facilities'] = facilDict
    except:
        print('Error in retrieving Facilities.')

    for facil in facilDict:
        facils = facilDict.get(facil)
        facilAvailability = facils.get_fac_status()
        if facilAvailability == 'Available':
            facilityUID = facils.get_uniqueID()
            facilityUIDList.append(facilityUID)
            facilityID = facils.get_fac_id()
            facilityIDList.append(facilityID)
            
    print(facilityUIDList)
    print(facilityIDList)