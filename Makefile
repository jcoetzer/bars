all:
	mkdir -p /opt/bars/bin
	find ./bin/ -name "*.py" -print -exec cp {} /opt/bars/bin/ \;
	mkdir -p /opt/bars/lib
	find ./lib/ -maxdepth 1 -name "*.py" -print -exec cp {} /opt/bars/lib/ \;
	mkdir -p /opt/bars/lib/Booking
	find ./lib/Booking -maxdepth 1 -name "*.py" -print -exec cp {} /opt/bars/lib/Booking \;
	mkdir -p /opt/bars/lib/Flight
	find ./lib/Flight -maxdepth 1 -name "*.py" -print -exec cp {} /opt/bars/lib/Flight \;
	mkdir -p /opt/bars/lib/Ssm
	find ./lib/Ssm -maxdepth 1 -name "*.py" -print -exec cp {} /opt/bars/lib/Ssm \;
	find ./etc/ -name "*.lst" -print -exec cp {} /opt/bars/etc/ \;
	find ./etc/ -name "*.cfg" -print -exec cp {} /opt/bars/etc/ \;

install:
	mkdir -p /opt/bars/sql
	find ./sql -name "*.sql" -print -exec cp {} /opt/bars/sql/ \;

clean:
	find . -name "*.pyc" -print -delete
	find /opt/bars/lib/ -name "*.py" -print -delete
	find /opt/bars/ -name "*.pyc" -print -delete
