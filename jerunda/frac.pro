TEMPLATE = app
TARGET = frac
INCLUDEPATH += . include src

# The following define makes your compiler warn you if you use any
# feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

QT+= core widgets gui

OBJECTS_DIR = objs/
MOC_DIR = mocs/
#DESTDIR = bin/
CONFIG += warn_on qt
CONFIG -= debug_and_release

QMAKE_LIBS += -lgomp -fopenmp
QMAKE_CFLAGS += -fopenmp

# Input
HEADERS += \
	include/window.h \
	include/picture.h \
	include/F.h \
	include/H.h

SOURCES += \
	src/frac.cpp \
	src/window.cpp \
	src/picture.c \
	src/F.c \
	src/H.c
