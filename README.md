# dex_of
This is an OpenFOAM automation interface for finding lift/drag forces and coefficients for 
arbritrary shaped submerged bodies. OpenFOAM's SnappyHexMesh and SimpleFOAM are used for 
computations. dex_of scripts automates the generation of the computational box, assignment of
boundary conditions, meshing, analysis and post-processing. It produces lift-drag coefficients
and forces on the boday. 

Provided to performers of the DARPA/SymCPS program.



To rebuild the docker image kishorestevens/dexof:latest  use build.sh
./build.sh

If you want to call the image something else, Change the image label inside the script.

Stevens-built docker image
I)	docker run --rm -v ${PWD}:/home/aimed_user/dexof_work kishorestevens/dexof  /home/aimed_user/dex_of/setup_dexof.sh
II)	cd ./test_casestudy
III) ./run_dexof.sh rough_mesh_8cores.dex seaglider.stl 1  
