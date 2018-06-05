# @file PricingData.py


import os
import sys
from datetime import datetime, timedelta, date

from BarsLog import printlog
from ReadDateTime import ReadDate
       

class FarePricingData(object):
    
    def __init__(self, 
                 fare_code,            
                 city_pair,
                 valid_from_date,
                 valid_to_date,
                 fare_value,
                 short_description,
                 onw_return_ind,
                 byps_strt_auth_level,
                 byps_end_auth_level,
                 selling_class):
        self.fare_code =            fare_code,           
        self.city_pair =            city_pair
        self.valid_from_date =      valid_from_date
        self.valid_to_date =        valid_to_date
        self.fare_value =           fare_value
        self.short_description =    short_description
        self.onw_return_ind =       onw_return_ind
        self.byps_strt_auth_level =   byps_strt_auth_level
        self.byps_end_auth_level =    byps_end_auth_level
        self.selling_class =        selling_class
        
    def display(self):
        print "Fare data:"
        print "\tFare code %s class %s value %.2f" % (self.fare_code, self.selling_class, self.fare_value)
        
             
class PricingData(object):
    
    pax_codes = []

    def __init__(self, 
                 total_amount,
                 tax_total_amount, 
                 fare_total_amount,
                 paxcodes):
        self.total_amount      = float(total_amount)
        self.fare_total_amount = float(fare_total_amount)
        self.tax_total_amount  = float(tax_total_amount)
        self.pax_codes         = paxcodes  
        printlog("New pricing amount %.2f" % (self.total_amount), 2)
    
    def display(self, prefix='\t'):  
        print "Pricing data:"
        print "*\tTotal           : R%.2f" % self.total_amount
        print "\tFare total      : R%.2f" % self.fare_total_amount
        print "\tTax total       : R%.2f" % self.tax_total_amount
        print "\tPassenger codes :"
        for pax_code in self.pax_codes:
            pax_code.display()
        
class PassengerCode(object):
    
    fare_codes = []
    tax_codes = [] 
    
    def __init__(self, 
                 passenger_code, 
                 seat_count, 
                 fare_value_per_seat,
                 surcharge_per_seat, 
                 tax_value_per_seat, 
                 fare_ladder, 
                 farecodes, 
                 taxcodes):
        self.passenger_code      = passenger_code     
        self.seat_count          = int(seat_count)
        self.fare_value_per_seat = float(fare_value_per_seat)
        self.surcharge_per_seat  = float(surcharge_per_seat) 
        self.tax_value_per_seat  = float(tax_value_per_seat)
        self.fare_ladder         = fare_ladder      
        self.fare_codes          = farecodes       
        self.tax_codes           = taxcodes
        printlog("New passenger code %s count %d value %.2f" \
            % (self.passenger_code, self.seat_count, self.fare_value_per_seat), 2)
        
    def display(self):
        print "\t*\tPassenger code      : %s" % self.passenger_code     
        print "\t\tSeat count          : %d" % self.seat_count         
        print "\t\tFare value per seat : %.2f" % self.fare_value_per_seat
        print "\t\tSurcharge per seat  : %.2f" % self.surcharge_per_seat 
        print "\t\tTax value per seat  : %.2f" % self.tax_value_per_seat 
        print "\t\tFare ladder         : %s" % self.fare_ladder
        print "\t\tFare codes :"
        for fare_code in self.fare_codes:
            fare_code.display()
        print "\t\tTax codes :"
        for tax_code in self.tax_codes:
            tax_code.display()
    
    
class FareCode(object):
    
    company_code   = 'ZZ'
    fare_code      = ''
    class_code     = 'Y'
    passenger_code = 'ADULT'
    base_amount    = 0.00
    fare_route_id  = ''
    valid_from     = ''
    valid_to       = ''
    flights        = []
    flight_codes = []
    
    def __init__(self, company_code, fare_code, class_code, passenger_code, base_amount, \
            fare_route_id, valid_from, valid_to, flightcodes):
        self.company_code   = company_code  
        self.fare_code      = fare_code        
        self.class_code     = class_code       
        self.passenger_code = passenger_code   
        self.base_amount    = float(base_amount)
        self.fare_route_id  = fare_route_id
        self.valid_from = ReadDate(valid_from)
        self.valid_to   = ReadDate(valid_to)
        self.flight_codes = flightcodes
        printlog("New fare code %s class %s ID %s" % (self.fare_code, self.class_code, self.fare_route_id), 2)
        
    def display(self, prefix='\t'):  
        print "\t\t*\tFare code       : %s" % self.fare_code
        print "\t\t\tCompany code    : %s" % self.company_code
        print "\t\t\tClass code      : %s" % self.class_code
        print "\t\t\tPassenger code  : %s" % self.passenger_code
        print "\t\t\tBase amount     : R%.2f" % self.base_amount
        print "\t\t\tFare route ID   : %s" % self.fare_route_id
        print "\t\t\tValid from      : %s" % self.valid_from.strftime("%Y-%m-%d")
        print "\t\t\tValid to        : %s" % self.valid_to.strftime("%Y-%m-%d")
        print "\t\t\tFlight codes :"
        for flight_code in self.flight_codes:
            flight_code.display()
  
  
class FlightCode(object):
    
    flight_no = ''
    flight_date = None
    airport_codes = []
    
    def __init__(self, flight_no, flight_date, airport_codes):
        self.flight_no = flight_no
        self.flight_date = flight_date
        self.airport_codes = airport_codes
        printlog("New flight code %s date %s " % (self.flight_no, self.flight_date), 2)
        
    def display(self, prefix='\t'):
        print "\t\t\t*\tFlight no     : %s" % self.flight_no
        print "\t\t\t\tFlight date   : %s" % self.flight_date
        print "\t\t\t\tAirport codes : "
        for airport_code in self.airport_codes:
            print "\t\t\t\t\tAirport code : %s" % airport_code


class TaxCode(object):
    
    def __init__(self, company_code, tax_code, coverage_type, coverage_value, description, \
                 tax_type, tax_value, tax_amount, detailid, flight_number, departure_date, \
                 departure_airport, arrival_airport):
        self.company_code       = company_code  
        self.tax_code           = tax_code      
        self.coverage_type      = coverage_type 
        self.coverage_value     = coverage_value
        self.description        = description   
        self.tax_type           = tax_type           
        self.tax_value          = tax_value          
        self.tax_amount         = tax_amount        
        self.detailid           = detailid          
        self.flight_number      = flight_number 
        self.departure_date     = ReadDate(departure_date)
        self.departure_date_iso = self.departure_date.strftime("%Y-%m-%d")
        self.departure_airport  = departure_airport 
        self.arrival_airport    = arrival_airport
        self.segments = [ 1 ]
        printlog("New tax code %s (%s)" % (self.tax_code, self.description), 2)
    
    def display(self, prefix='\t'):
       print "\t\t*\tTax code          : %s" % self.tax_code
       print "\t\t\tCompany code      : %s" % self.company_code
       print "\t\t\tCoverage type     : %s" % self.coverage_type
       print "\t\t\tCoverage value    : %s" % self.coverage_value
       print "\t\t\tDescription       : %s" % self.description
       print "\t\t\tTax type          : %s" % self.tax_type           
       print "\t\t\tTax value         : %s" % self.tax_value          
       print "\t\t\tTax amount        : %s" % self.tax_amount        
       print "\t\t\tDetail id         : %s" % self.detailid          
       print "\t\t\tFlight number     : %s" % self.flight_number 
       print "\t\t\tDeparture date    : %s" % self.departure_date_iso
       print "\t\t\tDeparture airport : %s" % self.departure_airport 
       print "\t\t\tArrival airport   : %s" % self.arrival_airport    

