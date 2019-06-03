#include"picture.h"

int bounds(struct Fractal * fractal)
{
	fractal->minY = -(fractal->maxX-fractal->minX)*((float)fractal->height/fractal->width)/2+fractal->offset;
	fractal->maxY = (fractal->maxX-fractal->minX)*((float)fractal->height/fractal->width)/2+fractal->offset;
	return 0;
}

int build(struct Fractal * fractal)
{
	int k; double delta; double start_time;
	delta = (fractal->maxX-fractal->minX)/fractal->width;

	start_time = omp_get_wtime();
#pragma omp parallel for 
	for(k=0; k<(fractal->height)*(fractal->width); k++){
		//if(k%1000==0) printf("%d ",k/1000);
		fractal->bitmap[k] = Iterate((fractal->minX+(k%fractal->width)*delta),
					(fractal->maxY-(k/fractal->width)*delta),
					fractal->constRe, fractal->constIm, fractal->deph);
	}

	printf("%lf\n", (omp_get_wtime()-start_time));

	return 0;
}
