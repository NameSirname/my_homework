#include<complex.h>
#include<math.h>
double G(double ,double,double _Complex);

double G(double i,double deph, double _Complex z){
        return -0.7*i+carg(1/ccos(z*z))*deph/6/i+ sin(cabs(z)/carg(z))*deph/3/i+ cabs(z)*deph/10/i;
}