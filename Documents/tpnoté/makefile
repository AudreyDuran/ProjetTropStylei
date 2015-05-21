all: teststring

teststring: teststring.cpp cstring.o
	g++ -Wall -o teststring.o teststring.cpp cstring.o

cstring.o: cstring.h cstring.cpp
	g++ -Wall -c -o cstring.o cstring.cpp

clean:
	rm *.o
go:
	./teststring.o


