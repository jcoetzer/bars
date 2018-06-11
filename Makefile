BARSDIR = /opt/bars

PYTHONS = ./bin/FlightDetailsService.pyc \
	./bin/SsmInfo.pyc \
	./bin/ProcSsm.pyc \
	./bin/BarsBook.pyc \
	./bin/BookInfo.pyc \
	./bin/FlightInfo.pyc \
	./bin/BarsFlight.pyc \
	./lib/Booking/ItenaryData.pyc \
	./lib/Booking/__init__.pyc \
	./lib/Booking/BookingSummaryXml.pyc \
	./lib/Booking/ReadItenary.pyc \
	./lib/Booking/ReadRequests.pyc \
	./lib/Booking/PricingData.pyc \
	./lib/Booking/BookingInfo.pyc \
	./lib/Booking/BookingPayment.pyc \
	./lib/Booking/FareCalcDisplay.pyc \
	./lib/Booking/ReadBooking.pyc \
	./lib/Booking/ReadCrossRef.pyc \
	./lib/Booking/GraphBookings.pyc \
	./lib/Booking/ReadBookSummary.pyc \
	./lib/Booking/ReadBookingRef.pyc \
	./lib/Booking/ReadTimeLimit.pyc \
	./lib/Flight/WriteFares.pyc \
	./lib/Flight/__init__.pyc \
	./lib/Flight/ReadFlightDateLegs.pyc \
	./lib/Flight/FlightData.pyc \
	./lib/Flight/AvailDb.pyc \
	./lib/Flight/ReadFlights.pyc \
	./lib/Flight/ReadFlightPeriods.pyc \
	./lib/Flight/ReadSeatMap.pyc \
	./lib/Flight/FlightDetails.pyc \
	./lib/Flight/ReadFlightLegs.pyc \
	./lib/Flight/ReadFlightSegments.pyc \
	./lib/Flight/ReadFlightTimes.pyc \
	./lib/Flight/ReadSchedPeriod.pyc \
	./lib/Flight/ReadFares.pyc \
	./lib/Ssm/__init__.pyc \
	./lib/Ssm/ReadSsmData.pyc \
	./lib/Ssm/SsmDb.pyc \
	./lib/Ssm/ProcCnl.pyc \
	./lib/Ssm/ProcNew.pyc \
	./lib/Ssm/ReadAircraftConfig.pyc \
	./lib/Ssm/ReadSsm.pyc \
	./lib/Ssm/SsmData.pyc \
	./lib/Ssm/SsmLex.pyc \
	./lib/Ssm/SsmYacc.pyc \
	./lib/Ssm/parsetab.pyc \
	./lib/BarsLog.pyc \
	./lib/ReadDateTime.pyc \
	./lib/BarsConfig.pyc \
	./lib/DbConnect.pyc \
	./lib/__init__.pyc \
	./lib/BarsBanner.pyc

#	./tmp/PaymentReminder.pyc

all: $(PYTHONS)


install: $(PYTHONS)
	mkdir -p $(BARSDIR)/bin
	find ./bin/ -name "*.py" -print -exec cp {} $(BARSDIR)/bin/ \;
	mkdir -p $(BARSDIR)/lib
	find ./lib/ -maxdepth 1 -name "*.py" -print -exec cp {} $(BARSDIR)/lib/ \;
	mkdir -p $(BARSDIR)/lib/Booking
	find ./lib/Booking -maxdepth 1 -name "*.py" -print -exec cp {} $(BARSDIR)/lib/Booking \;
	mkdir -p $(BARSDIR)/lib/Flight
	find ./lib/Flight -maxdepth 1 -name "*.py" -print -exec cp {} $(BARSDIR)/lib/Flight \;
	mkdir -p $(BARSDIR)/lib/Ssm
	find ./lib/Ssm -maxdepth 1 -name "*.py" -print -exec cp {} $(BARSDIR)/lib/Ssm \;
	find ./etc/ -name "*.lst" -print -exec cp {} $(BARSDIR)/etc/ \;
	find ./etc/ -name "*.cfg" -print -exec cp {} $(BARSDIR)/etc/ \;
	mkdir -p $(BARSDIR)/sql
	find ./sql -name "*.sql" -print -exec cp {} $(BARSDIR)/sql/ \;
	mkdir -p $(BARSDIR)/etc
	find ./etc -type f -print -exec cp {} $(BARSDIR)/etc/ \;

uninstall:
	find $(BARSDIR)/bin/ -name "*.py" -print -delete
	find $(BARSDIR)/lib/ -name "*.py" -print -delete
	find $(BARSDIR)/etc/ -type f -print -delete

clean:
	find . -name "*.pyc" -print -delete
	find $(BARSDIR)/ -name "*.pyc" -print -delete

%.pyc: %.py
	@python3 -m compileall $*.py
