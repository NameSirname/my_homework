#include"picture.h"
#include<stdlib.h>

int bounds(struct Fractal * fractal)
{
	fractal->minY = -(fractal->maxX-fractal->minX)*((float)fractal->height/fractal->width)/2+fractal->offset;
	fractal->maxY = (fractal->maxX-fractal->minX)*((float)fractal->height/fractal->width)/2+fractal->offset;
	return 0;
}

int build(struct Fractal * fractal)
{
	int k; double delta;
	delta = (fractal->maxX-fractal->minX)/fractal->width;

//#pragma omp parallel for//schedule(dynamic)
	for(k=0; k<(fractal->height)*(fractal->width); k++){
		fractal->bitmap[k] = H((fractal->minX+(k%fractal->width)*delta),
					(fractal->maxY-(k/fractal->width)*delta),
					fractal->constRe, fractal->constIm, fractal->deph);
	}

	/*double *sum;
	sum = (double*)malloc(10000000*sizeof(double));
#pragma omp parallel for//schedule(dynamic)
	for(k=0;k<10000000;k++) sum[k]=sqrt(k);*/

	return 0;
}
