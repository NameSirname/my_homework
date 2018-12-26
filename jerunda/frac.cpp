#include<QApplication>
#include"window.h"

int main(int argc, char *argv[])
{
	QApplication::setApplicationName("Fractal");
	QApplication app(argc, argv);

	Window Win;
	Win.initGUI();

	Win.SIZE(0,3,50000,50000);
	Win.DRAW(2);
	Win.DEPH(4,3,10000);
	Win.CONSTANT(5,-0.745,0.115);
	Win.BOUNDS(7,3,-1.5,1.5,0);
	Win.ZOOM(9);
	Win.FUNCTIONS(10, "z*z+c","i+cabs(z)*(deph/10/(i+1))","z = F(z,c);\nif (cabs(z)>5) break;");
	Win.Enter();
	
	Win.show();

	app.exec();

	free(Win.fractal.bitmap);
	return 0;
}


