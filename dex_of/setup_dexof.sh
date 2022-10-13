#!/bin/bash

echo "******************************************"
echo "**     DEXTER-OPENFOAM INTERFACE        **"
echo "**  Stevens Institute of Technology     **"
echo "**  No warranties: use at your own risk **"
echo "******************************************"


# Run this like this.
# docker run --rm -v ${PWD}:/home/aimed_user/dexof_work kishorestevens/dexof /home/aimed_user/dex_of/setup_dexof.sh
# chmod u+rx ./setup_dexof.sh  --> Copies a test case study and the script to run it.
# cd ./test_casestudy
# chmod a+rx ./run_dexof.sh
# ./run_dexof.sh <dexfile> <stlfile> <aoa>


cp -r /home/aimed_user/test_casestudy .
cp /home/aimed_user/dex_of/run_dexof.sh  ./test_casestudy
cp /home/aimed_user/dex_of/run_dexof_axisymmetric.sh  ./test_casestudy
cp -r /home/aimed_user/documentation .

echo " Notes: "
echo " A) cd to test_casestudy folder"
echo " B) To compute cl/cd on the seaglider.stl example, run"
echo " ./run_dexof.sh <dexfile> <stlfile> <aoa_in_degrees>"
echo " where <dexfile> is the the configuration file,"
echo " <stlfile> is the submerged object"
echo " <aoa_in_degree> is the angle of attack in degrees"
echo " -----------------------------------------------------"
echo " FOR EXAMPLE:"
echo "./run_dexof.sh rough_mesh_8cores.dex seaglider.stl 1  "
echo " RUNS seaglider with a coarse mesh and at 1 degree aoa. "
echo " -----------------------------------------------------"
echo "*** ALL DONE  ***"
