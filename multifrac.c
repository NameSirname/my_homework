#include<stdio.h>
#include<stdlib.h>
#include<complex.h>
#include<omp.h>

#include "multifrac_h.h"

int bitmap(int, int, int, double, double, double, double, double, double, double**);


int main(void){
	FILE *in,*out;
	int i,j, w,h,deph; double a11,a12,a21,a22,Rec,Imc, **B;
	in = fopen("in.txt","r");
	out = fopen("out.txt","w");
	
	fscanf(in,"%d%d%d%lf%lf%lf%lf%lf%lf",
		&w,&h,&deph,&a11,&a12,&a21,&a22,&Rec,&Imc);


	B = (double**)malloc(h*sizeof(double*));
	for(i=0;i<h;i++) B[i]=(double*)malloc(w*sizeof(double));

	bitmap(w,h,deph,a11,a12,a21,a22,Rec,Imc,B);

	for(i=0;i<h;i++){
		for(j=0;j<w;j++) fprintf(out,"%.10lf ",B[i][j]);
		fprintf(out,"\n");
	}
	free(B);
	fclose(in); fclose(out);
	return 0;
}

int bitmap(int w, int h, int deph, double a11, double a12, double a21, double a22, double Rec, double Imc,double **B){
	int i; double delta1,delta2;
	
	delta1 = (a21-a11)/(w-1);
	delta2 = (a12-a22)/(h-1);


#pragma omp parallel for schedule(dynamic)
	for(i=0;i<h*w;i++){
		B[i/w][i%w] = H((a11+(i%w)*delta1) + (a22+(i/w)*delta2) * I, Rec + Imc*I, deph);
	}
	return 0;

}



