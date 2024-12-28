# Makefile located in the root directory

# Compiler and flags
CXX = C:/mingw32/bin/g++  # 明示的に旧リポジトリのMinGWパスを指定
INCLUDES = -I./include -I./include/test_framework -I./include/mem_allocator -I./include/data_structures -I./include/dx
CXXFLAGS = $(INCLUDES) -DDX_GCC_COMPILE
LDFLAGS = -L./lib -lDxLib -lDxUseCLib -lDxDrawFunc -ljpeg -lpng -lzlib -ltiff -ltheora_static -lvorbis_static -lvorbisfile_static -logg_static -lbulletdynamics -lbulletcollision -lbulletmath -lopusfile -lopus -lsilk_common -lcelt -lm -lstdc++

SRCDIR = ./src
TESTDIR = ./test
BUILDDIR = ./build
TARGET = run
TEST_TARGET = run_test

# Source files
SRCS := $(wildcard $(SRCDIR)/*.cpp) $(wildcard $(SRCDIR)/*/*.cpp)
TESTS := $(wildcard $(TESTDIR)/*.cpp)

# Remove App/main.cpp from test object files
SRCS_NO_MAIN := $(filter-out $(SRCDIR)/App/main.cpp,$(SRCS))

# Object files
OBJFILES := $(SRCS:$(SRCDIR)/%.cpp=$(BUILDDIR)/%.o)
TEST_OBJFILES := $(SRCS_NO_MAIN:$(SRCDIR)/%.cpp=$(BUILDDIR)/%.test.o) $(TESTS:$(TESTDIR)/%.cpp=$(BUILDDIR)/%.test.o)

# Default target
all: $(TARGET)

# Production build
$(TARGET): $(OBJFILES)
	$(CXX) -o $@ $(OBJFILES) $(LDFLAGS)

# Test build
$(TEST_TARGET): $(TEST_OBJFILES)
	$(CXX) -o $@ $(TEST_OBJFILES) $(LDFLAGS)

# Compile each source file to an object file
$(BUILDDIR)/%.o: $(SRCDIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Compile each source file to a test object file with UNIT_TEST_BUILD macro defined
$(BUILDDIR)/%.test.o: $(SRCDIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Compile each test file to a test object file
$(BUILDDIR)/%.test.o: $(TESTDIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Clean up build artifacts
clean:
	rm -rf $(BUILDDIR)/*.o $(BUILDDIR)/*.test.o $(TARGET) $(TEST_TARGET)

.PHONY: all clean test

# Test build target
test: $(TEST_TARGET)
