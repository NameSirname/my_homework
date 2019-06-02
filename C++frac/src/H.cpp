#include"H.h"

unsigned char H(double zRe, double zIm , double cRe, double cIm, int deph){
	int k;
	double _Complex z = zRe+zIm*I, c = cRe+cIm*I;
	for(k=0;k<deph;k++){
		z = F(z,c);
		if(cabs(z)>5) break;
	}
	return (unsigned char)k;
}

