#!/bin/bash
echo "Dex_of Openfoam Automation Docker Builder"
echo "Zipping the code"
tar -czf ./dex_of.tgz ./Dex_of
echo "Zip the example file "
tar -czf ./testcase.tgz  ./test_casestudy
docker build . -t kishorestevens/dexof:latest
