#!/bin/bash
echo "USAGE: postprocess.sh <dir> "
fname = $1
echo "*** PostProcessing ***"
cd $1
grep -H ells  $1.log  >> results.log
grep -H "Cl " $1.log >> results.log
grep -H "Cd " $1.log >> results.log
grep -H "Cs " $1.log >> results.log
grep -H "Finished meshing in"  log.snappy* >> results.log
grep -H "Execution"  $1.log  >> results.log
grep -H Aref postProcessing/forceCoeffs/0/coefficient.dat >> results.log
grep -H lRef postProcessing/forceCoeffs/0/coefficient.dat >> results.log
echo "Results stored in $1/results.log"
cat ./results.log
cd ..
echo "*** ALL DONE ***"
