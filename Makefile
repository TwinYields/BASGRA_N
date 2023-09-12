
lib:
	f2py -c  model/parameters_plant.f90 model/parameters_site.f90 \
    model/resources.f90 model/environment.f90 model/soil.f90 model/plant.f90 model/set_params.f90 \
    model/bglib.f90 -m bglib
	mv bglib.cpython*.so basgrapy

basgra: BASGRA.so
	gfortran -fpic -x f95-cpp-input -O3 -c -fdefault-real-8 model/parameters_site.f90 \
 		model/parameters_plant.f90 model/environment.f90 model/resources.f90 model/soil.f90 \
 		model/plant.f90 model/set_params.f90 model/BASGRA.f90
	gfortran -fpic -shared -o BASGRA.so parameters_site.o parameters_plant.o environment.o resources.o soil.o plant.o set_params.o BASGRA.o
	rm -f *.o
	rm -f *.mod

all: lib basgra

clean:
	rm -f model/*.mod
	rm -f model/*.so
	rm -f model/*.o