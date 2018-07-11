## -*- coding: utf-8 -*-
## -------------------------------------------------------------------------
## BARS Airline Reservation Simulator
##
## this file is released under public domain and you can use without limitations
## -------------------------------------------------------------------------

import os
from datetime import date, datetime, time, timedelta

from BarsConfig import BarsConfig
from Booking.BookingHtml import GetAvailHtml, GetPriceHtml, PutBookHtml
from ReadDateTime import ReadDate


def index():
    """ Index page."""
    response.flash = T("BARS Airline Reservation Simulator")
    #form = FORM(INPUT(_name='depart', requires=IS_NOT_EMPTY()),
                #INPUT(_name='arrive', requires=IS_NOT_EMPTY()),
                #INPUT(_name='fdate', requires=IS_NOT_EMPTY()),
                #INPUT(_type='submit'))
    ## if form.process().accepted:
    #if form.vars.depart is not None:
        #print("Form accepted")
        #session.depart = form.vars.depart
        #session.arrive = form.vars.arrive
        #session.date = form.vars.date
        #redirect(URL('availability'))
        ##return dict(form=form)
    #else:
        #print("Form not quite right")
    redirect(URL('availability'))
    #return dict()


def availability():
    """Flight availability query."""
    return dict()


def availshow():
    """Get availability information."""
    vCompany = 'ZZ'
    departAirport = str(request.vars.depart)
    arriveAirport = str(request.vars.arrive)
    fdate = ReadDate(request.vars.fdate)
    msg = GetAvailHtml(conn, fdate, fdate,
                       departAirport, arriveAirport,
                       vCompany, '/bars/default/priceshow')
    return dict(message=XML(msg))


def priceshow():
    """Display flight prices."""
    flightNumber = str(request.vars.fnumber)
    flightDate = ReadDate(request.vars.fdate)
    departAirport = str(request.vars.depart)
    arriveAirport = str(request.vars.arrive)
    sellClass = 'Y'
    msg = GetPriceHtml(conn,
                       cfg.CompanyCode,
                       departAirport, arriveAirport,
                       flightDate, flightDate,
                       sellClass,  # cfg.SellingClass,
                       cfg.OnwReturnIndicator,
                       cfg.FareCategory,
                       cfg.AuthorityLevel)
    return dict(message=XML(msg))


def booking():
    """Input number of seats e.a. for booking."""
    msg = "<p/>Book flight"
    return dict(message=XML(msg))


def bookingnames():
    """Input names e.a. for booking."""
    flightNumber = str(request.vars.fnumber)
    flightDate = ReadDate(request.vars.fdate)
    departAirport = str(request.vars.depart)
    arriveAirport = str(request.vars.arrive)
    seatCount = int(request.vars.fseats)
    sellClass = request.vars.fclass
    groupName = ''
    msg = "<p/>Book flight"
    return dict(message=XML(msg))


def bookingshow():
    """Process booking."""
    flightNumber = str(request.vars.fnumber)
    flightDate = ReadDate(request.vars.fdate)
    departAirport = str(request.vars.depart)
    arriveAirport = str(request.vars.arrive)
    seatCount = int(request.vars.fseats)
    sellClass = request.vars.fclass
    groupName = ''
    payAmount = 0.0
    paxRecs = []
    timeLimit = datetime.now() + timedelta(days=2)
    passenger_code = 'ADULT'
    passenger_no = 1
    paxname = '%s/%s %s' % (request.vars.paxlname1,
                            request.vars.paxfname1.replace(' ', ''),
                            request.vars.paxtitle1)
    date_of_birth = request.vars.paxdob1
    contact_phone = request.vars.bkcell
    contact_email = request.vars.bkemail
    pax = PassengerData(passenger_code, passenger_no, paxname,
                        date_of_birth, contact_phone, contact_email)
    paxRecs.append(pax)
    msg = "<p/>Booked flight"
    msg += PutBook(conn, cfg.CompanyCode, cfg.BookCategory, cfg.OriginAddress,
                   cfg.OriginBranchCode, cfg.AgencyCode,
                   groupName, paxRecs,
                   cfg.Currency, payAmount,
                   flightNumber, flightDate,
                   departAirport, arriveAirport,
                   sellClass, cfg.FareBasisCode,
                   timeLimit,
                   cfg.User, cfg.Group)
    return dict(message=XML(msg))


## ---- API (example) -----
#@auth.requires_login()
#def api_get_user_email():
    #if not request.env.request_method == 'GET': raise HTTP(403)
    #return response.json({'status':'success', 'email':auth.user.email})


## ---- Smart Grid (example) -----
#@auth.requires_membership('admin') # can only be accessed by members of admin groupd
#def grid():
    #response.view = 'generic.html' # use a generic view
    #tablename = request.args(0)
    #if not tablename in db.tables: raise HTTP(403)
    #grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    #return dict(grid=grid)


## ---- Embedded wiki (example) ----
#def wiki():
    #auth.wikimenu() # add the wiki to the menu
    #return auth.wiki()


## ---- Action for login/register/etc (required for auth) -----
#def user():
    #"""
    #exposes:
    #http://..../[app]/default/user/login
    #http://..../[app]/default/user/logout
    #http://..../[app]/default/user/register
    #http://..../[app]/default/user/profile
    #http://..../[app]/default/user/retrieve_password
    #http://..../[app]/default/user/change_password
    #http://..../[app]/default/user/bulk_register
    #use @auth.requires_login()
        #@auth.requires_membership('group name')
        #@auth.requires_permission('read','table name',record_id)
    #to decorate functions that need access control
    #also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    #"""
    #return dict(form=auth())


## ---- action to server uploaded static content (required) ---
#@cache.action()
#def download():
    #"""
    #allows downloading of uploaded files
    #http://..../[app]/default/download/[filename]
    #"""
    #return response.download(request, db)
