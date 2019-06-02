#pragma once
#ifndef window_h 
#define window_h

#include"picture.h"
#include<stdlib.h>

#include<QMainWindow>
#include<QWidget>
#include<QGridLayout>

#include<QLineEdit>
#include<QTextEdit>
#include<QLabel>
#include<QPushButton>
#include<QSpinBox>
#include<QDoubleSpinBox>
#include<QComboBox>
#include<QCheckBox>

#include<QVector>
#include<QImage>
#include<Qt>
#include<QApplication>
#include<QMouseEvent> 
//#include<QColor>
//#include<QPalette>

#include<QCoreApplication>

//#include"colormaps.hpp"

class Window : public QMainWindow
{	Q_OBJECT
	public:
		QPoint pos = QPoint(0,0);
		QSize size = QSize(925,700);
		int toolbar_width = 225;
		int row_num = 5;
		bool zooming = 0;
		QPoint mousePressCoords;
		
		QWidget * toolbar;
		QGridLayout * grid;
		QSpinBox * Width, * Height;
		QCheckBox * plot;
		QSpinBox * deph;
		QDoubleSpinBox * constRe, * constIm;
		QLineEdit * F, * G; QCheckBox * f, * g;
		QTextEdit * H; QCheckBox * h;
		QDoubleSpinBox * a, * c, * d;

		struct Fractal fractal;	
		QLabel * imageLabel;
		
		void initGUI();
		void initFractal();
		void SIZE(int,int,int,int);
		void DEPH(int,int,int);
		void CONSTANT(int,double,double);
		void BOUNDS(int,int,double,double,double);
		void FUNCTIONS(int,const char *,const char *,const char *);
		void DRAW(int);
		void ZOOM(int);
		
		void drawImage();

	public slots:
		void Resize();
		void Enter();
		void Zoom();

	protected:
		virtual void mousePressEvent(QMouseEvent *);
		virtual void mouseReleaseEvent(QMouseEvent *);
};

#endif

