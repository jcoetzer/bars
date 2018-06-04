BARSDIR = /opt/bars

all:
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

install:
	mkdir -p $(BARSDIR)/sql
	find ./sql -name "*.sql" -print -exec cp {} $(BARSDIR)/sql/ \;
	find ./etc -type f -print -exec cp {} $(BARSDIR)/etc/ \;

uninstall:
	find $(BARSDIR)/bin/ -name "*.py" -print -delete
	find $(BARSDIR)/lib/ -name "*.py" -print -delete
	find $(BARSDIR)/etc/ -type f -print -delete

clean:
	find . -name "*.pyc" -print -delete
	find $(BARSDIR)/ -name "*.pyc" -print -delete
