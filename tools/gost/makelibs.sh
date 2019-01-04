#!/usr/bin/env sh

libs=$((for file in `ls lib` ; do echo "./lib/$file" ; done) | tr "[:space:]" ":")
#libs=./lib/UcrelSemTaggerClient.jar:./lib/discriminator-2.3.3.jar:./lib/jackson-databind-2.9.7.jar:./lib/serialization-2.6.0.jar
echo "export libs=$libs"
