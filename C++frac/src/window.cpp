#include"window.h"

#define uchar unsigned char

void Window::initGUI()
{	
	resize(size);
	move(pos);

	toolbar = new QWidget(this);
	toolbar->resize(toolbar_width,size.height());
	toolbar->move(pos);
	toolbar->setStyleSheet(".QWidget {background-color: #123;}");	

	imageLabel = new QLabel(this);
	imageLabel->resize(size.width()-toolbar_width, size.height());
	imageLabel->move(pos.x()+toolbar_width,pos.y());

	grid = new QGridLayout(toolbar);
	grid->setSpacing(10);
	toolbar->setLayout(grid);
}

void Window::initFractal()
{
	fractal.width = imageLabel->width();
	fractal.height = imageLabel->height();
	fractal.minX = a->value();
	fractal.maxX = c->value();
	fractal.offset = d->value();
	bounds(&fractal);
	fractal.constRe = constRe->value();
	fractal.constIm = constIm->value();
	fractal.deph = deph->value();

	fractal.bitmap = (uchar *)malloc((fractal.width)*(fractal.height)*sizeof(uchar));
}
//________________________________________________________

void Window::DRAW(int position)
{
	QPushButton * resize = new QPushButton("Resize", this);
	QObject::connect(resize,SIGNAL(clicked()),this,SLOT(Resize()));
	grid->addWidget(resize,position,0,1,row_num);

	QPushButton * enter = new QPushButton("Draw", this);
	QObject::connect(enter, SIGNAL(clicked()),this, SLOT(Enter()));
	grid->addWidget(enter,position+1,0,1,row_num-1);

	plot = new QCheckBox(this);
	plot->setCheckState(Qt::Checked);
	grid->addWidget(plot,position+1,row_num-1,1,1);
}

void Window::ZOOM(int position)
{
	QPushButton * zoom = new QPushButton("Zoom", this);
	QObject::connect(zoom, SIGNAL(clicked()),this, SLOT(Zoom()));
	grid->addWidget(zoom,position,0,1,row_num);
}
/*
void Window::SAVE(this,position)
	{
	Save = QPushButton('Save', this)
	Save.clicked.connect(Save)
	grid.addWidget(Save,position,0,1,row_num)
	SaveAnim = QPushButton('SaveAnimation', this)
	SaveAnim.clicked.connect(SaveAnimation)
	grid.addWidget(SaveAnim,position+1,0,1,row_num)
}
*/
void Window::SIZE(int position, int rows, int MaxWidth, int MaxHeight)
{
	Width = new QSpinBox(this);
	Width->setRange(size.width(),MaxWidth);
	Width->setValue(size.width());
	Width->setSingleStep(10);
	grid->addWidget(Width,position,0,1,rows);

	Height = new QSpinBox(this);
	Height->setRange(size.height(),MaxHeight);
	Height->setValue(size.height());
	Height->setSingleStep(10);
	grid->addWidget(Height,position+1,0,1,rows);

	QLabel * width_l = new QLabel("width");
	width_l->setStyleSheet("color: rgba(255,255,255)");
	grid->addWidget(width_l,position,rows,1,row_num-rows);

	QLabel * height_l = new QLabel("height");
	height_l->setStyleSheet("color: rgba(255,255,255)");
	grid->addWidget(height_l,position+1,rows,1,row_num-rows);
}

void Window::DEPH(int position, int rows,int MaxDeph)
{
	deph = new QSpinBox(this);
	deph->setRange(1,MaxDeph);
	deph->setValue(200);
	grid->addWidget(deph,position,0,1,rows);

	QLabel * deph_l = new QLabel("deph");
	deph_l->setStyleSheet("color: rgba(255,255,255)");
	grid->addWidget(deph_l,position,rows,1,row_num-rows);
}

void Window::CONSTANT(int position, double DefaultConstReal, double DefaultConstImag)
{
	constRe = new QDoubleSpinBox(this);
	constRe->setRange(-1000,1000);
	constRe->setDecimals(15);
	constRe->setSingleStep(0.001);
	constRe->setValue(DefaultConstReal);
	grid->addWidget(constRe,position,0,1,row_num-1);
 
	constIm = new QDoubleSpinBox(this);
	constIm->setRange(-1000,1000);
	constIm->setDecimals(15);
	constIm->setSingleStep(0.001);
	constIm->setValue(DefaultConstImag);
	grid->addWidget(constIm,position+1,0,1,row_num-1);
   
	QLabel * const_lRe = new QLabel("Re(c)");
	const_lRe->setStyleSheet("color: rgba(255,255,255)");
	grid->addWidget(const_lRe,position,row_num-1,1,1);

	QLabel * const_lIm = new QLabel("Im(c)");
	const_lIm->setStyleSheet("color: rgba(255,255,255)");
	grid->addWidget(const_lIm,position+1,row_num-1,1,1);
}

void Window::FUNCTIONS(int position,
  const char * DefaultF,
  const char * DefaultG,
  const char * DefaultH)
{
	F = new QLineEdit(this);
	F->setText(DefaultF);
	grid->addWidget(F,position,0,1,row_num-1);

	f = new QCheckBox(this);
	f->setCheckState(Qt::Unchecked);
	grid->addWidget(f,position,row_num-1,1,1);

	G = new QLineEdit(this);
	G->setText(DefaultG);
	grid->addWidget(G,position+1,0,1,row_num-1);

	g = new QCheckBox(this);
	g->setCheckState(Qt::Unchecked);
	grid->addWidget(g,position+1,row_num-1,1,1);

	H = new QTextEdit(this);
	H->setText(DefaultH);
	grid->addWidget(H,position+2,0,1,row_num-1);

	h = new QCheckBox(this);
	h->setCheckState(Qt::Unchecked);
	grid->addWidget(h,position+2,row_num-1,1,1);
}

void Window::BOUNDS(int position, int rows, double minX, double maxX, double offset)
{
	a = new QDoubleSpinBox(this);
	a->setDecimals(10);
	a->setRange(-1000,1000);
	a->setSingleStep(0.01);
	a->setValue(minX);
	grid->addWidget(a,position,0,1,rows);

	c = new QDoubleSpinBox(this);
	c->setDecimals(10);
	c->setRange(-1000,1000);
	c->setSingleStep(0.01);
	c->setValue(maxX);
	grid->addWidget(c,position+1,0,1,rows);

	d = new QDoubleSpinBox(this);
	d->setDecimals(6);
	d->setRange(-1000,1000);
	d->setSingleStep(0.01);
	d->setValue(offset);
	grid->addWidget(d,position+1,rows,1,row_num-rows);

	QLabel * d_l = new QLabel("offset");
	d_l->setStyleSheet("color: rgba(255,255,255)");
	grid->addWidget(d_l,position,rows,1,row_num-rows);
}
/*
void Window::COLORMAP(this,position,DefaultMap = 'p2', DefaultColorMaps = []):
{
	CMap = QComboBox(this)
	CMap.addItems(DefaultColorMaps)
	CMap.addItems(my_cmaps.A)
	CMap.setCurrentText(DefaultMap)
	CMap.activated.connect(Change_colormap)
	grid.addWidget(CMap,position,0,1,row_num-1)
	CMap.l = QLabel('cmap')
	CMap.l.setStyleSheet("color: rgba(255,255,255)")
	grid.addWidget(CMap.l,position,row_num-1,1,1)
}
void Window::ANIMATE(this,position,rows, DefaultSpeed = '250',
DefaultDelta = 'c-0.01j')
{
	Animate = QPushButton('Animate', this)
	Animate.clicked.connect(Animate)
	grid.addWidget(Animate,position,0,1,rows)
	frames = QLineEdit('2',this)
	grid.addWidget(frames,position,rows,1,row_num-rows)
	delta = QLineEdit(DefaultDelta,this)
	grid.addWidget(delta,position+1,0,1,rows)
	speed = QLineEdit(DefaultSpeed,this)
	grid.addWidget(speed,position+1,rows,1,row_num-rows)
}*/

//________________________________________________________
void Window::Resize()
{	
	size = QSize(Width->value(),Height->value());
	//pos = QPoint(0,0);
	resize(size);
	//move(pos);

	toolbar->resize(toolbar_width,size.height());
	//toolbar->move(pos);

	imageLabel->resize(size.width()-toolbar_width,size.height());
	//imageLabel->move(pos.x()+toolbar_width,pos.y());
}
void Window::Enter()
{	
	//int res;
	//res = std::system("g++ -c -pipe -O2 -D_REENTRANT -Wall -W -fPIC -DQT_DEPRECATED_WARNINGS -DQT_NO_DEBUG -DQT_WIDGETS_LIB -DQT_GUI_LIB -DQT_CORE_LIB -I. -I. -Iinclude -Isrc src/F.c -o objs/F.o");
	//printf("%d\n",res);
	this->initFractal();
	this->drawImage();
	//free(fractal.bitmap);
}

void Window::Zoom()
{	
	zooming = !zooming;
	if(zooming) QApplication::setOverrideCursor(Qt::CrossCursor);
	else QApplication::setOverrideCursor(Qt::ArrowCursor);
}

//________________________________________________________
void Window::mousePressEvent(QMouseEvent * event)
{
	if(zooming) mousePressCoords = event->pos();
}

void Window::mouseReleaseEvent(QMouseEvent * event)
{
	if(zooming){
		a->setValue(fractal.minX+(float)(mousePressCoords.x()-toolbar_width)/fractal.width*(fractal.maxX-fractal.minX));
		c->setValue(fractal.minX+(float)(event->x()-toolbar_width)/fractal.width*(fractal.maxX-fractal.minX));
		d->setValue(fractal.maxY-(float)(mousePressCoords.y()+event->y())/2/fractal.height*(fractal.maxY-fractal.minY));
	}
}
//________________________________________________________

void Window::drawImage()
{
	QVector<QRgb> palette;
	int k, stride = fractal.width;
	build(&fractal);

	for(k=0;k<deph->value();k++) palette.push_back(qRgb(k/2, k ,k*k%255));

	QImage picture = QImage(fractal.bitmap, fractal.width, fractal.height, stride, QImage::Format_Indexed8);	
	picture.setColorTable(palette);
	picture = picture.convertToFormat(QImage::Format_RGB32);
	imageLabel->setPixmap(QPixmap::fromImage(picture));
}

