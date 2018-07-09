BARSDIR = /opt/bars
WEB2PYDIR = /opt/web2py

PYTHONS = \
	./bin/BarsBook.pyc \
	./bin/BarsFlight.pyc \
	./bin/BookInfo.pyc \
	./bin/FlightDetailsService.pyc \
	./bin/FlightInfo.pyc \
	./bin/PnlGen.pyc \
	./bin/ProcSsm.pyc \
	./bin/SsmInfo.pyc \
	./lib/BarsBanner.pyc \
	./lib/BarsConfig.pyc \
	./lib/BarsLog.pyc \
	./lib/Booking/BookingInfo.pyc \
	./lib/Booking/BookingPayment.pyc \
	./lib/Booking/FareCalcDisplay.pyc \
	./lib/Booking/__init__.pyc \
	./lib/Booking/ItineraryData.pyc \
	./lib/Booking/PassengerData.pyc \
	./lib/Booking/PaymentData.pyc \
	./lib/Booking/PricingData.pyc \
	./lib/Booking/ReadBooking.pyc \
	./lib/Booking/ReadBookingRef.pyc \
	./lib/Booking/ReadBookSummary.pyc \
	./lib/Booking/ReadCrossRef.pyc \
	./lib/Booking/ReadItinerary.pyc \
	./lib/Booking/ReadRequests.pyc \
	./lib/Booking/ReadTimeLimit.pyc \
	./lib/DbConnect.pyc \
	./lib/Flight/AvailDb.pyc \
	./lib/Flight/FlightData.pyc \
	./lib/Flight/FlightDetails.pyc \
	./lib/Flight/__init__.pyc \
	./lib/Flight/ReadFares.pyc \
	./lib/Flight/ReadFlightBookings.pyc \
	./lib/Flight/ReadFlightDateLegs.pyc \
	./lib/Flight/ReadFlightLegs.pyc \
	./lib/Flight/ReadFlightPeriods.pyc \
	./lib/Flight/ReadFlightSegments.pyc \
	./lib/Flight/ReadFlights.pyc \
	./lib/Flight/ReadFlightTimes.pyc \
	./lib/Flight/ReadSchedPeriod.pyc \
	./lib/Flight/ReadSeatMap.pyc \
	./lib/Flight/ReadTaxes.pyc \
	./lib/Flight/WriteFares.pyc \
	./lib/__init__.pyc \
	./lib/PnlAdl/PaxData.pyc \
	./lib/PnlAdl/PaxListEntry.pyc \
	./lib/PnlAdl/PaxList.pyc \
	./lib/PnlAdl/ReadPnl.pyc \
	./lib/ReadDateTime.pyc \
	./lib/ScheduleData.pyc \
	./lib/Ssm/AircraftData.pyc \
	./lib/Ssm/__init__.pyc \
	./lib/Ssm/parsetab.pyc \
	./lib/Ssm/ProcCnl.pyc \
	./lib/Ssm/ProcNew.pyc \
	./lib/Ssm/ReadAircraftConfig.pyc \
	./lib/Ssm/ReadSsmData.pyc \
	./lib/Ssm/ReadSsm.pyc \
	./lib/Ssm/SsmData.pyc \
	./lib/Ssm/SsmDb.pyc \
	./lib/Ssm/SsmLex.pyc \
	./lib/Ssm/SsmYacc.pyc \

all: $(PYTHONS)

install: $(PYTHONS)
	@mkdir -p $(BARSDIR)
	rsync --exclude=__pycache__ -av bin $(BARSDIR)
	rsync --exclude=__pycache__ -av lib $(BARSDIR)
	rsync --exclude=__pycache__ -av sql $(BARSDIR)
	rsync --exclude=__pycache__ -av etc $(BARSDIR)
	rsync --exclude=__pycache__ -av www/applications/bars $(WEB2PYDIR)/applications

uninstall:
	find $(BARSDIR)/bin/ -name "*.py" -print -delete
	find $(BARSDIR)/lib/ -name "*.py" -print -delete
	find $(BARSDIR)/etc/ -type f -print -delete
	find $(BARSDIR)/ -name "*.pyc" -print -delete

clean:
	find . -name "*.pyc" -print -delete

%.pyc: %.py
	@python3 -m compileall $*.py
