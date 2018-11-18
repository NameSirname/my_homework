#include<complex.h>
#include<math.h>
double G(int ,int ,double complex);

double G(int i,int deph ,double complex z){
        return i+cabs(z)*(deph/10/i+10);
}