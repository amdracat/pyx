# Makefile located in the root directory

# Compiler and flags
CC = gcc
INCLUDES = -I./include -I./include/test_framework -I./include/mem_allocator -I./include/data_structures
CFLAGS = $(INCLUDES)
TEST_CFLAGS = $(INCLUDES) -DUNIT_TEST_BUILD
SRCDIR = ./src
TESTDIR = ./test
BUILDDIR = ./build
TARGET = run
TEST_TARGET = run_test

# Source files
SRCFILES := $(wildcard $(SRCDIR)/*.c) $(wildcard $(SRCDIR)/*/*.c)
TESTFILES := $(wildcard $(TESTDIR)/*.c)

# Remove App/main.c from test object files
SRCFILES_NO_MAIN := $(filter-out $(SRCDIR)/App/main.c,$(SRCFILES))

# Object files
OBJFILES := $(SRCFILES:$(SRCDIR)/%.c=$(BUILDDIR)/%.o)
TEST_OBJFILES := $(SRCFILES_NO_MAIN:$(SRCDIR)/%.c=$(BUILDDIR)/%.test.o) $(TESTFILES:$(TESTDIR)/%.c=$(BUILDDIR)/%.test.o)

# Default target
all: $(TARGET)

# Production build
$(TARGET): $(OBJFILES)
	$(CC) -o $@ $(OBJFILES)

# Test build
$(TEST_TARGET): $(TEST_OBJFILES)
	$(CC) -o $@ $(TEST_OBJFILES)

# Compile each source file to an object file
$(BUILDDIR)/%.o: $(SRCDIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c -o $@ $<

# Compile each source file to a test object file with UNIT_TEST_BUILD macro defined
$(BUILDDIR)/%.test.o: $(SRCDIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(TEST_CFLAGS) -c -o $@ $<

# Compile each test file to a test object file
$(BUILDDIR)/%.test.o: $(TESTDIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(TEST_CFLAGS) -c -o $@ $<

# Clean up build artifacts
clean:
	rm -rf $(BUILDDIR)/*.o $(BUILDDIR)/*.test.o $(TARGET) $(TEST_TARGET)

.PHONY: all clean test

# Test build target
test: $(TEST_TARGET)
