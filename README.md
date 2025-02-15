# dex_of
This is an OpenFOAM automation interface for finding lift/drag forces and coefficients for 
arbritrary shaped submerged bodies. OpenFOAM's SnappyHexMesh and SimpleFOAM are used for 
computations. dex_of scripts automate the generation of the computational box, assignment of
boundary conditions, meshing, analysis, and post-processing. It produces lift-drag coefficients
and forces on the body. 


Originally created for the performers in the DARPA/SymCPS program.

Disclaimer:  Check the underlying assumptions of the 
SimpleFOAM solutions. Results may be highly mesh senstitive for some geometries.
Be sure to ascertain the the validity of the results. 

How to use:
1. Source files are needed only if you want to change/modify dex_of. Users do not need to download the source.
2. Install docker desktop on your system
3. Use the Stevens-built docker image to run dex_of on your system. Note there may be permission issues on Linux to run docker. 
4. on MacOS and Linux hosts, the following commands will work. See the full instructions in the documentation folder
5. Run the commands below to get an example test case and have the docker image set up.
6. 
 docker run --rm -v ${PWD}:/home/aimed_user/dexof_work kishorestevens/dexof  /home/aimed_user/dex_of/setup_dexof.sh

 cd ./test_casestudy
 
 ./run_dexof.sh rough_mesh_8cores.dex seaglider.stl 1

8.  Flow direction is +x of the STL. Length units are meters. Use scalex,scaley, scalez parameters in the dex file to scale your stl.


Building Custom Docker Images. 

1. To rebuild the docker image kishorestevens/dexof:latest, clone or fork this repo, and  use build.sh 

./build.sh

2. If you want to call the image something else, edit the label in the build.sh script.

http://prooflab.stevens.edu
