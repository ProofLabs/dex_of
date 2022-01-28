#!/bin/bash
echo "USAGE: postprocess.sh <dir> "
cd $1
echo "*** PostProcessing ***"
echo "*** Results ***" >> results.log
echo " ----- LIFT AND DRAG FORCES ---- " >> results.log
tail -13 log.simpleFoam |head -8 >> results.log
echo " ----- LIFT AND DRAG COEFFICIENTS ---- " >> results.log
tail -50 log.simpleFoam | grep "Cd       :" |tail -1 >> results.log
tail -50 log.simpleFoam | grep "Cl       :" |head -1 >> results.log
tail -50 log.simpleFoam | grep "Cs       :" |head -1 >> results.log
echo "___ REFERENCE AREAS ----" >> results.log
echo "Arefs" >> results.log
find ./postProcessing -name "coefficient.dat" -exec grep -H Aref {} \; >> results.log
echo "lrefs:" >> results.log
find ./postProcessing -name "coefficient.dat" -exec grep -H lRef {} \; >> results.log
echo "----- MESH DENSITIES & CPU TIMES ----- "
grep -H ells  $(basename $1).log  >> results.log
grep -H "Finished meshing in"  log.snappyHexMesh >> results.log
grep "Time =" log.simpleFoam | tail -2 >> results.log
echo "Results stored in $(basename $1)/results.log"
cd ..
echo "*** ALL DONE ***"
