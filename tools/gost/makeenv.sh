#!/usr/bin/env sh

libs=$((for file in `ls lib` ; do echo "./lib/$file" ; done) | tr "[:space:]" ":")
echo "LIBS=$libs"
