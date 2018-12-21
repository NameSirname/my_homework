#include<complex.h>
#include<math.h>

#include "multifrac_f.h"
#include "multifrac_g.h"

double H(double _Complex, double _Complex, int);

double H(double _Complex z, double _Complex c, int deph){
        int k; _Complex w;
	w=z; z = c;
	for (k=1;k<=deph;k++){
	z = F(z,w);
	if (cabs(z)>5) break;
	}
	return G((double)k,(double)deph,z);
}
