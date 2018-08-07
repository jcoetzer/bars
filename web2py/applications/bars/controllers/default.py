## -*- coding: utf-8 -*-
## -------------------------------------------------------------------------
## BARS Airline Reservation Simulator
##
## this file is released under public domain and you can use without limitations
## -------------------------------------------------------------------------

import os
import logging
import random
from datetime import date, datetime, time, timedelta

from BarsConfig import BarsConfig
from Booking.BookingHtml import GetAvailHtml, GetPriceHtml, PutBookHtml, \
    PutPayHtml
from ReadDateTime import ReadDate
from Booking.PassengerData import PassengerData

logger = logging.getLogger("web2py.app.bars")

def index():
    """ Index page."""
    #logger.debug("Start")
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
    logger.debug("Availability")
    return dict()


def availshow():
    """Get availability information."""
    logger.debug("Show availability")
    vCompany = 'ZZ'
    departAirport = str(request.vars.depart)
    arriveAirport = str(request.vars.arrive)
    flightDate = ReadDate(request.vars.fdate)
    logger.debug("Get availability for date %s depart %s arrive %s"
                  % (flightDate, departAirport, arriveAirport))
    msg = GetAvailHtml(conn, flightDate, flightDate,
                       departAirport, arriveAirport,
                       vCompany, '/bars/default/priceshow')
    conn.commit()
    return dict(message=XML(msg))


def priceshow():
    """Display flight prices."""
    logger.debug("Show prices")
    flightNumber = str(request.vars.fnumber)
    flightDate = ReadDate(request.vars.fdate)
    departAirport = str(request.vars.depart)
    arriveAirport = str(request.vars.arrive)
    sellClass = 'Y'
    logger.debug("Get price for date %s depart %s arrive %s"
                  % (flightDate, departAirport, arriveAirport))
    msg, amt = GetPriceHtml(conn,
                            cfg.CompanyCode,
                            departAirport, arriveAirport,
                            flightDate, flightDate,
                            sellClass,  # cfg.SellingClass,
                            cfg.OnwReturnIndicator,
                            cfg.FareCategory,
                            cfg.AuthorityLevel)
    conn.commit()
    return dict(message=XML(msg), amount=amt)


def booking():
    """Input number of seats e.a. for booking."""
    logger.debug("Book flight")
    msg = "<p/>Book flight"
    return dict(message=XML(msg))


def bookingnames():
    """Input names e.a. for booking."""
    logger.debug("Booking names")
    flightNumber = str(request.vars.fnumber)
    flightDate = ReadDate(request.vars.fdate)
    departAirport = str(request.vars.depart)
    arriveAirport = str(request.vars.arrive)
    seatPrice = float(request.vars.fprice)
    seatCount = int(request.vars.fseats[0])
    sellClass = request.vars.fclass
    bookAmount = float(seatCount * seatPrice)
    groupName = ''
    logger.debug("Get %s names for flight %s date %s depart %s arrive %s"
                 % (seatCount, flightNumber, flightDate, departAirport, arriveAirport))
    msg = "<p/>Book flight"
    paxtitles = []
    paxfnames = []
    paxlnames = []
    paxdobs = []
    paxRecs = []
    if request.vars.nfake == 'on':
        i = 1
        while i <= seatCount:
            paxRec = PassengerData('ADULT', i)
            paxRec.fakeit(cfg.DialCode)
            paxRecs.append(paxRec)
            i += 1
        for paxRec in paxRecs:
            paxtitles.append(paxRec.passenger_title)
            paxfnames.append(paxRec.first_name)
            paxlnames.append(paxRec.last_name)
            paxdobs.append(paxRec.date_of_birth)
    else:
        i = 1
        while i <= seatCount:
            paxtitles.append('')
            paxfnames.append('')
            paxlnames.append('')
            paxdobs.append('')
            i += 1

    return dict(message=XML(msg), amount=bookAmount,
                titles=paxtitles, fnames=paxfnames, lnames=paxlnames,
                dobs=paxdobs)


def bookingshow():
    """Process booking."""
    logger.debug("Show new booking")
    flightNumber = str(request.vars.fnumber)
    flightDate = ReadDate(request.vars.fdate)
    departAirport = str(request.vars.depart)
    arriveAirport = str(request.vars.arrive)
    seatCount = int(request.vars.fseats or 1)
    seatPrice = float(request.vars.fprice)
    payAmount = float(seatCount * seatPrice)
    sellClass = request.vars.fclass
    logger.debug("Book %s seats for flight %s date %s depart %s arrive %s"
                  % (seatCount, flightNumber, flightDate,
                     departAirport, arriveAirport))
    groupName = ''
    paxRecs = []
    timeLimit = datetime.now() + timedelta(days=2)
    passenger_code = 'ADULT'
    passenger_no = 1
    paxname = '%s/%s %s' % (request.vars.paxlname1,
                            request.vars.paxfname1.replace(' ', ''),
                            request.vars.paxtitle1)
    date_of_birth = ReadDate(request.vars.paxdob1)
    contact_phone = request.vars.bkcell
    contact_email = request.vars.bkemail
    pax = PassengerData(passenger_code, passenger_no, paxname,
                        date_of_birth, contact_phone, contact_email)
    logger.debug("Pax %s (born %s)" % (paxname, date_of_birth))
    paxRecs.append(pax)
    logger.debug("Process booking flight %s date %s"
                  % (flightNumber, flightDate))
    bn, pnr, msg = PutBookHtml(conn, cfg.CompanyCode, cfg.BookCategory, cfg.OriginAddress,
                               cfg.OriginBranchCode, cfg.AgencyCode,
                               groupName, paxRecs,
                               cfg.Currency, payAmount,
                               flightNumber, flightDate,
                               departAirport, arriveAirport,
                               sellClass, cfg.FareBasisCode,
                               timeLimit,
                               cfg.User, cfg.Group)
    #msg += "<p/>Booked flight"
    return dict(message=XML(msg), bookno=bn, locator=pnr, amount=payAmount)


def bookingpay():
    """Do payment for booking."""
    logger.debug("Booking payment")
    n = random.randint(0,100)
    if n < 5:  # cfg.PaymentFail:
        redirect(URL('bookingpayfail'))
    redirect(URL('bookingpayshow'))


def bookingpayfail():
    """Do payment for booking."""
    logger.debug("Booking payment failed")
    msg = "Payment declined."
    return dict(message=XML(msg))


def bookingpayshow():
    """Show payment for booking."""
    logger.debug("Show payment")
    bookNo = int(request.vars.bookno)
    sellClass = request.vars.fclass
    payAmount = float(request.vars.fprice)
    docNum = request.vars.cardnum
    paymentType = 'CC'
    paymentForm = 'VI'
    logger.debug("Payment for booking %d class %s %s%.2f %s card %s"
                  % (bookNo, sellClass, cfg.Currency, payAmount, paymentForm,
                     docNum))
    rv, msg = PutPayHtml(conn, bookNo, sellClass,
                         cfg.Currency, payAmount, 0.0,
                         cfg.CompanyCode, cfg.OriginBranchCode, cfg.FareBasisCode,
                         paymentType, paymentForm, docNum,
                         cfg.User, cfg.Group)
    if rv == 0:
        msg = "<p/>Payment approved."
    conn.commit()
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
