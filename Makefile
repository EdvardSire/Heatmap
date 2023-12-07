CC = clang
CCOPTS = -g
SRC = src
BUILD = build

all: main stat

main:
	$(CC) $(CCOPTS) $(SRC)/$@.c -o $(BUILD)/$@

stat:
	$(CC) $(CCOPTS) $(SRC)/$@.c -o $(BUILD)/$@


