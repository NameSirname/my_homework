#pragma once
#ifndef picture_h_
#define picture_h_
#include"Iterate.h"
#include<stdlib.h>
#include<time.h>
#include<omp.h>

struct Fractal{ 
	unsigned char * bitmap;
	double minX, maxX, minY, maxY, offset;
	double constRe, constIm;
	int width; int height;
	int deph;
};

int bounds(struct Fractal *);
int build(struct Fractal *);

#endif

