import subprocess as sub

def new_F(s):
    f_file = open("multifrac_f.h","w")
    f_file.write('''#include<complex.h>
#include<math.h>
double _Complex F(double _Complex,double _Complex);

double _Complex F(double _Complex z,double _Complex c){
        return %s;
}'''%(s))
    f_file.close()
    
    return None

def new_G(s):
    g_file = open("multifrac_g.h","w")
    g_file.write('''#include<complex.h>
#include<math.h>
double G(double ,double,double _Complex);

double G(double i,double deph, double _Complex z){
        return %s;
}'''%(s))
    g_file.close()
    
    return None

def new_H(s):
    h_file = open("multifrac_h.h","w")
    h_file.write('''#include<complex.h>
#include<math.h>

#include "multifrac_f.h"
#include "multifrac_g.h"

double H(double _Complex, double _Complex, int);

double H(double _Complex z, double _Complex c, int deph){
        %s
	return G((double)k,(double)deph,z);
}'''%(s))
    h_file.close()
    
    return None


        
def comp_le():
    p = sub.Popen(["gcc","-Wall","-Wextra","-fopenmp","multifrac.c",
                   "-lm","-o","a.o"],
                  stdout=sub.PIPE)
    p.communicate()
    return None
