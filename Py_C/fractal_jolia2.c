#include<stdio.h>
#include<stdlib.h>
#include<complex.h>

#include "fractal2.h"

int bitmap(int, int, int, double, double, double, double, double, double, FILE *);
double _Complex c;

int main(void){
	FILE *in,*out;
	int w,h,deph; double a11,a12,a21,a22,Rec,Imc;
	in = fopen("in.txt","r");
	out = fopen("out.txt","w");
	
	fscanf(in,"%d%d%d%lf%lf%lf%lf%lf%lf",
		&w,&h,&deph,&a11,&a12,&a21,&a22,&Rec,&Imc);
	bitmap(w,h,deph,a11,a12,a21,a22,Rec,Imc,out);

	fclose(in); fclose(out);
	return 0;
}

int bitmap(int w, int h, int deph, double a11, double a12, double a21, double a22, double Rec, double Imc, FILE * out){
	int i,j,k; double delta1,delta2;
	double _Complex z,c;
	c = Rec + Imc*I;

	delta1 = (a21-a11)/(w-1);
	delta2 = (a12-a22)/(h-1);
	for(i=0;i<h;i++){
		for(j=0;j<w;j++){
			z = (a11+j*delta1) + (a22+i*delta2) * I;
			for (k=0;k<deph;k++){
				z = F(z,c);
				if (cabs(z)>5) break;
			}
			fprintf(out,"%d ",k);
		}
		fprintf(out,"\n");
	}
	return i;

}

