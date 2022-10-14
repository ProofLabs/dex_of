#!/bin/bash
echo "******************************************"
echo "**     DEXTER-OPENFOAM INTERFACE        **"
echo "**  Stevens Institute of Technology     **"
echo "**  No warranties: use at your own risk **"
echo "******************************************"

echo "USAGE: run_dexof_axisymmetric.sh dexfile stlfile"
if [ -z "$1" ]
  then
    echo "No dex file is supplied"
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

docker run --rm -v ${PWD}:/home/aimed_user/dexof_work kishorestevens/dexof /home/aimed_user/dex_of/run_axisymmetric.sh $1 $2

echo "*** ALL DONE -- ALL DONE ***"
