#!/bin/bash


rm *.o
rm *.mod

#-fdefault-real-8
gfortran -x f95-cpp-input -O3 -c  parameters_site.f90 \
 parameters_plant.f90 environment.f90 resources.f90 soil.f90 \
 plant.f90 set_params.f90

f2py -c -I.  environment.o parameters_plant.o parameters_site.o \
 plant.f90  -m plant

#f2py -c -I.  parameters_plant.o parameters_site.o \
#environment.f90  -m environment
f2py parameters_plant.f90 parameters_site.f90 environment.f90  -m environment -h environment.pyf
f2py -c -I.  parameters_plant.f90 parameters_site.f90 environment.f90  -m environment

# python -c 'import plant'
# methods are under plant.plant

# F2PY basgra
#--f90flags='-x f95-cpp-input -fdefault-real-8'

f2py -c  -I. parameters_plant.o parameters_site.o \
    resources.o soil.o plant.o set_params.o \
    environment.f90 basgra.f90  -m basgra

#python -c 'import basgra; print("hello")'


f2py -c -I.  parameters_plant.f90 parameters_site.f90 environment.f90  -m environment