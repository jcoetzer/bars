all:
	find ./bin/ -name "*.py" -print -exec cp {} /opt/bars/bin/ \;
	find ./lib/ -name "*.py" -print -exec cp {} /opt/bars/lib/ \;
