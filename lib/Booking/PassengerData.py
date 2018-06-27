# @file PassengerData.py
"""
Passenger name, date of birth and contact details.
"""

import os
import sys
from random import randint

from BarsLog import printlog, get_verbose
from ReadDateTime import ReadDate
from faker import Faker

fake = Faker()

class PassengerInfo(object):

    def __init__(self, passenger_code, number_of_seats=1):
        self.passenger_code  = passenger_code
        self.number_of_seats = number_of_seats

    def display(self):
        print("Passenger code %s : %d seats"
              % (self.passenger_code, self.number_of_seats))


class PassengerCount(object):

    counts = {}
    count = 0

    def __init__(self):
        count += 1


class PassengerData(object):

    passenger_no = 0
    passenger_code = ''
    last_name = ''
    first_name = ''
    passenger_title = ''
    passenger_name = ''
    number_of_seats = 1
    processing_flg = 'Y'
    date_of_birth = None
    contact_phone = None
    contact_email = None

    def __init__(self, passenger_code, passenger_no=1, paxname=None,
                 date_of_birth=None, contact_phone=None, contact_email=None,
                 processing_flg='Y'):
        self.passenger_no = int(passenger_no)
        self.passenger_code = passenger_code
        if paxname is not None:
            self.passenger_name = paxname
            nameparts = paxname.split(' ')
            names = nameparts[0].split('/')
            self.last_name = names[0]
            if len(names) > 1:
                self.first_name = names[1]
            if len(nameparts) > 1:
                self.passenger_title = nameparts[1]
            else:
                self.passenger_title = ''
        if date_of_birth is not None:
            self.date_of_birth = date_of_birth
        if contact_phone is not None:
            self.contact_phone = contact_phone
        if contact_email is not None:
            self.contact_email = contact_email
        self.processing_flg = processing_flg

    def fakeit(self, aDialCode='+27', last_name=None):
        global fake
        if self.passenger_no % 2 == 0:
            self.first_name = fake.first_name_female()
            lnames = randint(0, 1)
            n = 0
            while n < lnames:
                self.first_name += ' ' + fake.first_name_female()
                n += 1
            if self.passenger_code == 'ADULT':
                self.last_name = fake.last_name_female()
                self.passenger_title = fake.prefix_female()
            else:
                self.last_name = last_name
                self.passenger_title = 'MISS'
        else:
            self.first_name = fake.first_name_male()
            lnames = randint(0, 2)
            n = 0
            while n < lnames:
                self.first_name += ' ' + fake.first_name_male()
                n += 1
            if self.passenger_code == 'ADULT':
                self.last_name = fake.last_name_male()
                self.passenger_title = fake.prefix_male()
            else:
                self.last_name = last_name
                self.passenger_title = 'MR'
        self.passenger_name = str(self.last_name + '/' +
                                  self.first_name.replace(' ', '') + ' '
            + self.passenger_title).upper().replace('.', '')
        if self.passenger_code == 'CHILD':
            self.date_of_birth = fake.date_between(start_date="-16y", end_date="-1y")
        else:
            self.date_of_birth = fake.date_between(start_date="-80y", end_date="-16y")
        self.contact_phone = aDialCode + fake.msisdn()[4:]
        self.contact_email = str(self.first_name.split(' ')[0] + self.last_name + '@'
                                 + fake.domain_name()).lower()

    def display(self, prefix='\t'):
        print("%sPassenger %d (paid %s %s) %s"
                % (prefix, self.passenger_no, self.processing_flg,
                    self.passenger_code,
                    self.passenger_name), end=' ')
        if self.date_of_birth is not None:
            dob = self.date_of_birth.strftime("%d%b%Y")
            print(": born %s" \
                   % (dob), end=' ')
        if self.contact_phone is not None \
        and self.contact_email is not None:
            print("phone %s email %s"
                  % (self.contact_phone, self.contact_email), end=' ')
        print('')
