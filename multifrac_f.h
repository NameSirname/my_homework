#include<complex.h>
#include<math.h>
double _Complex F(double _Complex,double _Complex);

double _Complex F(double _Complex z,double _Complex c){
        return z*z+c;
}