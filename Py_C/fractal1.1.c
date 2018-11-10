#include<stdio.h>
#include<stdlib.h>
#include<complex.h>

#include "fractal1.1.h"

int bitmap(int, int, int, double, double, double, double, double, double, int **);
double _Complex c;

int main(void){
	return 0;
}

int bitmap(int w, int h, int deph, double a11, double a12, double a21, double a22, double Rec, double Imc,int** B){
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
			B[i][j]=k;
		}
	}
	return i;

}

