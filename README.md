# dex_of

To rebuild the docker image kishorestevens/dexof:latest  use build.sh
./build.sh

If you want to call the image something else, Change the image label inside the script.

Stevens-built docker image
I)	docker run --rm -v ${PWD}:/home/aimed_user/dexof_work kishorestevens/dexof /home/aimed_user/dex_of/setup_dexof.sh
II)	cd ./test_casestudy
III) ./run_dexof.sh rough_mesh_8cores.dex seaglider.stl 1  
