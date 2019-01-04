#!/usr/bin/env sh

source ./libs.sh
echo $libs
groovy -cp $libs semtagger.groovy $1 $2
