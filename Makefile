CC = clang
CCOPTS = -g
SRC = src
BUILD = build

all: main stat

main:
	$(CC) $(CCOPTS) $(SRC)/$@.cc -o $(BUILD)/$@

stat:
	$(CC) $(CCOPTS) $(SRC)/$@.cc -o $(BUILD)/$@


