#ifndef picture_h_
#define picture_h_
#include"H.h"
//#include<omp.h>

#ifdef __cplusplus
extern "C" {
#endif
struct Fractal{ 
	unsigned char * bitmap;
	double minX, maxX, minY, maxY, offset;
	double constRe, constIm;
	int width; int height;
	int deph;
};

int bounds(struct Fractal *);
int build(struct Fractal *);
#ifdef __cplusplus
}
#endif

#endif
