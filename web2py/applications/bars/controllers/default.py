## -*- coding: utf-8 -*-
## -------------------------------------------------------------------------
## BARS Airline Reservation Simulator
##
## this file is released under public domain and you can use without limitations
## -------------------------------------------------------------------------

import os

from Ssm.SsmDb import GetCityPair
from Booking.BookingHtml import GetAvailHtml, GetPriceHtml
from DbConnect import OpenDb, CloseDb
from BarsConfig import BarsConfig
from ReadDateTime import ReadDate
from Flight.AvailDb import get_selling_conf, get_avail_flights, OldAvailSvc
from Booking.FareCalcDisplay import FareCalcDisplay, \
     ReadSellingConfig


#barsdir = os.environ['BARSDIR']
#etcdir = "%s/etc" % barsdir

#cfg = BarsConfig('%s/bars.cfg' % etcdir)

## Open connection to database
#conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

## ---- example index page ----
def index():
    response.flash = T("BARS Airline Reservation Simulator")
    form = FORM(INPUT(_name='depart', requires=IS_NOT_EMPTY()),
                INPUT(_name='arrive', requires=IS_NOT_EMPTY()),
                INPUT(_name='date', requires=IS_NOT_EMPTY()),
                INPUT(_type='submit'))
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
    return dict()


def availability():
    """Flight availability query."""
    return dict() # message=T(''))


def availshow():
    """Get availability information."""
    vCompany = 'ZZ'
    departAirport = str(request.vars.depart or "JNB")
    arriveAirport = str(request.vars.arrive or "GRJ")
    fdate = ReadDate(request.vars.date or "today")
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    flights = OldAvailSvc(conn, vCompany, fdate, cityPairNo,
                          departAirport, arriveAirport)
    msg = "<table>"
    for flight in flights:
        msg += flight.html('/bars/default/priceshow')
    msg += "<table>"
    #for selling_class in selling_classes:
        #flights = get_avail_flights(conn, dt1, dt2, cityPairNo,
                                    #departAirport, arriveAirport,
                                    #selling_class[0], vCompany)
        #for flight in flights:
            #flight.display()
    return dict(message=XML(msg))


def priceshow():
    departAirport = str(request.vars.depart or "JNB")
    arriveAirport = str(request.vars.arrive or "GRJ")
    fdate = ReadDate(request.vars.date or "today")
    sellClass = 'Y'

    msg = GetPriceHtml(conn,
                       cfg.CompanyCode,
                       departAirport, arriveAirport,
                       fdate, fdate,
                       sellClass,  # cfg.SellingClass,
                       cfg.OnwReturnIndicator,
                       cfg.FareCategory,
                       cfg.AuthorityLevel)
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

