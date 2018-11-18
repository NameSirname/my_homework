#include<complex.h>
#include<math.h>
double G(double ,double ,double _Complex);

double G(double i,double deph ,double _Complex z){
        return i+cabs(z)*(deph/10/i+10);
}
