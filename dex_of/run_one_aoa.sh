#!/usr/bin/openfoam2112

echo "USAGE: run_one_aoa.sh dexfile stlfile aoa "
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

if [ -z "$3" ]
  then
    echo " AOA is required "
    exit 2
fi

fname=`echo "$1" | cut -d'.' -f1`

echo $fname

echo "*** Preprocessing *** "
python /home/aimed_user/dex_of/dex_of.py  $1 --infile $2 --aoa $3 --casefoldername dir_${fname}_aoa_$3
cd dir_${fname}_aoa_$3
echo "*** Cleaning and Running OF ***"
./Allclean; ./Allrun &> dir_${fname}_aoa_$3.log
echo "*** PostProcessing ***"
grep -H ells  dir_${fname}_aoa_$3.log  >> results.log
grep -H "Cl " dir_${fname}_aoa_$3.log >> results.log
grep -H "Cd " dir_${fname}_aoa_$3.log >> results.log
grep -H "Cs " dir_${fname}_aoa_$3.log >> results.log
grep -H "Finished meshing in"  log.snappyHexMesh >> results.log
grep -H "Execution"  dir_${fname}_aoa_$3.log  >> results.log
grep -H Aref postProcessing/forceCoeffs/0/coefficient.dat >> results.log
grep -H lRef postProcessing/forceCoeffs/0/coefficient.dat >> results.log
echo "Results stored in dir_${fname}_aoa_$3/results.log"
cat ./results.log
cd ..
echo "*** ALL DONE ***"
