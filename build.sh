#!/bin/bash
echo "Dex_of Openfoam Automation Docker Builder"
echo "Zipping the code"
tar -czf ./dex_of.tgz ./Dex_of
echo "Zip the example files and documentation "
tar -czf ./testcase.tgz  ./test_casestudy
tar -czf ./docs.tgz ./documentation

# Change the docker image name below if you want to call it something else.
docker build . -t kishorestevens/dexof:latest
#
