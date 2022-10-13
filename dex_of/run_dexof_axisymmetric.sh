#!/usr/bin/openfoam2112

echo "USAGE: run_dexof_axisymmetric.sh dexfile stlfile"
if [ -z "$1" ]
  then
    echo "No dex file is not supplied"
    exit 1
fi

if [[ $1 != *.dex ]]
    then
        echo "First Argument must be a .dex file"
        exit 2
    fi
if [ -z "$2" ]
  then
    echo " STL file is required "
    exit 2
fi

if [[ $2 != *.stl ]]
    then
        echo "Second argument must be a .stl file"
        exit 2
    fi

fname=`echo "$1" | cut -d'.' -f1`

echo "Running openfoam in Docker "

echo $fname

echo "*** Preprocessing *** "
python /home/aimed_user/dex_of/dex_of.py  $1 --infile $2 --casefoldername dir_${fname}_axisymmetric --axisymmetric
cd dir_${fname}_axisymmetric
echo "*** Cleaning and Running OF ***"
./Allclean; ./Allrun &> dir_${fname}_axisymmetric.log
echo "*** PostProcessing ***"
echo "*** Results ***" >> results.log
echo " ----- DRAG FORCES ---- " >> results.log
tail -13 log.simpleFoam |head -8 >> results.log
echo " ----- LIFT AND DRAG COEFFICIENTS ---- " >> results.log
tail -50 log.simpleFoam | grep "Cd       :" |tail -1 >> results.log
echo "___ REFERENCE AREAS ----" >> results.log
echo "Arefs" >> results.log
find ./postProcessing -name "coefficient.dat" -exec grep -H Aref {} \; >> results.log
echo "----- MESH DENSITIES & CPU TIMES ----- "
grep -H ells  dir_${fname}_axisymmetric.log  >> results.log
grep -H "Finished meshing in"  log.snappyHexMesh >> results.log
echo " Converged In:"
grep "Time =" log.simpleFoam | tail -2 >> results.log
echo "Results stored in dir_${fname}_axisymmetric/results.log"
cat ./results.log
cd ..
echo "*** ALL DONE -- ALL DONE ***"
