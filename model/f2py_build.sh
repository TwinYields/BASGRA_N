#!/bin/bash


rm *.o
rm *.mod


gfortran -x f95-cpp-input -O3 -c -fdefault-real-8 parameters_site.f90 \
 parameters_plant.f90 environment.f90 resources.f90 soil.f90 \
 plant.f90 set_params.f90

f2py -c --f90flags='-fdefault-real-8' -I.  environment.o parameters_plant.o parameters_site.o \
 plant.f90  -m plant

# python -c 'import plant'
# methods are under plant.plant

# F2PY basgra

f2py -c --f90flags='-x f95-cpp-input -fdefault-real-8' -I. parameters_plant.o parameters_site.o \
    resources.o soil.o plant.o set_params.o \
    environment.f90 basgra.f90  -m basgra

#python -c 'import basgra; print("hello")'




