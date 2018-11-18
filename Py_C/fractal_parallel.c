#include<stdio.h>
#include<stdlib.h>
#include<complex.h>
#include<omp.h>

#include "fractal_parallel.h"

int bitmap(int, int, int, double, double, double, double, double, double, int**);

int calculate(_Complex, int);
double _Complex c;

int main(void){
	FILE *in,*out;
	int i,j, w,h,deph,**B; double a11,a12,a21,a22,Rec,Imc;
	in = fopen("in.txt","r");
	out = fopen("out.txt","w");
	
	fscanf(in,"%d%d%d%lf%lf%lf%lf%lf%lf",
		&w,&h,&deph,&a11,&a12,&a21,&a22,&Rec,&Imc);


	B = (int**)malloc(h*sizeof(int*));
	for(i=0;i<h;i++) B[i]=(int*)malloc(w*sizeof(int));

	bitmap(w,h,deph,a11,a12,a21,a22,Rec,Imc,B);


	for(i=0;i<h;i++){
		for(j=0;j<w;j++) fprintf(out,"%d ",B[i][j]);
		fprintf(out,"\n");
	}
	free(B);
	fclose(in); fclose(out);
	return 0;
}

int bitmap(int w, int h, int deph, double a11, double a12, double a21, double a22, double Rec, double Imc,int **B){
	int i; double delta1,delta2;
	c = Rec + Imc*I;
	
	delta1 = (a21-a11)/(w-1);
	delta2 = (a12-a22)/(h-1);


#pragma omp parallel for schedule(dynamic)
	for(i=0;i<h*w;i++){
		B[i/h][i%w] = calculate((a11+(i%w)*delta1) + (a22+(i/h)*delta2) * I,deph);
	}
	return 0;

}
int calculate(_Complex z,int deph){
	int k;
	for (k=1;k<=deph;k++){
		z = F(z,c);
		if (cabs(z)>5) break;
	}
	return k;
}
