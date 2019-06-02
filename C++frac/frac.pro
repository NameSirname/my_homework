TEMPLATE = app
TARGET = frac
INCLUDEPATH += . include src

DEFINES += QT_DEPRECATED_WARNINGS

QT+= core widgets gui

#DESTDIR = bin/
OBJECTS_DIR = obj/
INCLUDE_DIR = include/
SOURCE_DIR = src/
MOC_DIR = moc/
CONFIG += warn_on qt
CONFIG -= debug_and_release

QMAKE_LIBS += -fopenmp #-lgomp
QMAKE_CXXFLAGS += -fopenmp
QMAKE_LFLAGS += -fopenmp

# Input
HEADERS += \
	$${INCLUDE_DIR}/window.h \
	$${INCLUDE_DIR}/picture.h \
	$${INCLUDE_DIR}/F.h \
	$${INCLUDE_DIR}/H.h

SOURCES += \
	$${SOURCE_DIR}/frac.cpp \
	$${SOURCE_DIR}/window.cpp \
	$${SOURCE_DIR}/picture.cpp \
	$${SOURCE_DIR}/F.cpp \
	src/H.cpp
