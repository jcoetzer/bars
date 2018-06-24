BARSDIR = /opt/bars

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
	find $(BARSDIR)/ -name "*.pyc" -print -delete

clean:
	find . -name "*.pyc" -print -delete

%.pyc: %.py
	@python3 -m compileall $*.py
