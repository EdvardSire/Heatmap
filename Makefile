# Compiler and flags
CC = gcc
CXX = g++
CFLAGS = -Wall
CXXFLAGS = -Wall

# Directories
SRCDIR = src
BUILDDIR = build

# Find all C and C++ source files
CFILES := $(wildcard $(SRCDIR)/*.c)
CPPFILES := $(wildcard $(SRCDIR)/*.cpp)

# Generate corresponding executable names
CEXECUTABLES := $(patsubst $(SRCDIR)/%.c, $(BUILDDIR)/%, $(CFILES))
CPPEXECUTABLES := $(patsubst $(SRCDIR)/%.cpp, $(BUILDDIR)/%, $(CPPFILES))

# Targets
all: $(CEXECUTABLES) $(CPPEXECUTABLES)

# Compile and link C source files
$(BUILDDIR)/%: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) $< -o $@

# Compile and link C++ source files
$(BUILDDIR)/%: $(SRCDIR)/%.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

# Clean rule
clean:
	rm -rf $(BUILDDIR)/*

