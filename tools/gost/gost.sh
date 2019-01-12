#!/usr/bin/env sh

#source ./libs.sh
#echo $libs
java -cp .:lib/* semtagger $1 $2
